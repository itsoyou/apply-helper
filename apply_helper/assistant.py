from apply_helper.config import logger, Config
import time

def create_assistant():
    assistant = Config.CLIENT.beta.assistants.create(
        name="File-based Assistant",
        instructions='Please provide a human-written cover letter for the given job description using persona that has skills mentioned in uploaded resume in PDF file. Also give me interview questions that hiring manager might ask for 40 mins of interview for this person for the position described in the job description.',
        model="gpt-4o-mini",
        tools=[{"type": "file_search"}],
    )
    logger.debug("Assistant created with ID: %s", assistant.id)
    return assistant.id


def run_assistant(thread_id, assistant_id):
    response = Config.CLIENT.beta.threads.runs.create(
        thread_id=thread_id, assistant_id=assistant_id
    )
    logger.debug("Assistant run response: %s", response)
    return response


def checking_status(thread_id, run_id, timeout=30, polling_interval=2):
    try:
        start_time = time.time()
        while True:
            logger.debug("thread_id: %s", thread_id)
            logger.debug("run_id: %s", run_id)
            run_object = Config.CLIENT.beta.threads.runs.retrieve(
                thread_id=thread_id, run_id=run_id
            )
            status = run_object.status
            logger.debug("Current status: %s", status)

            # Check if run is complete or failed
            if status == "completed":
                thread_messages = Config.CLIENT.beta.threads.messages.list(thread_id)
                answers = []

                for message in thread_messages.data:
                    if message.role == "assistant":
                        for content_item in message.content:
                            if content_item.type == "text":
                                answers.append(content_item.text.value.strip())
                logger.debug("Answers: %s", answers)
                return answers[0] if answers else None
            
            # Check for failed or cancelled states
            elif status in ["failed", "cancelled", "expired"]:
                logger.error("Run failed with status: %s", status)
                return None

            # Check timeout
            if time.time() - start_time > timeout:
                logger.error("Timeout waiting for response")
                return None

            # Wait before polling again
            time.sleep(polling_interval)

    except Exception as e:
        logger.error("Error checking status or retrieving messages: %s", e)
        return None


def create_thread():
    thread = Config.CLIENT.beta.threads.create()
    logger.debug("Thread created with ID: %s", thread.id)
    return thread.id


def add_question(thread_id, question):
    response = Config.CLIENT.beta.threads.messages.create(
        thread_id=thread_id, role="user", content=question
    )
    return response
