import os
import time

from openai import OpenAI

print(os.environ.get("OPENAI_API_KEY"))

MATH_ASSISTANT_ID = "asst_hIMerViwV6zSBwJKFNPnXg1s"

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def submit_message(assistant_id, thread, user_message):
    client.beta.threads.messages.create(
        thread_id=thread.id, role="user", content=user_message
    )
    print("DEBUG: " + thread.id)
    return client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id,
    )

def get_response(thread):
    return client.beta.threads.messages.list(thread_id=thread.id, order="asc")

def create_thread_and_run(user_input):
    thread = client.beta.threads.create()
    run = submit_message(MATH_ASSISTANT_ID, thread, user_input)
    return thread, run

thread1, run1 = create_thread_and_run(
    "I need to solve the equation `3x + 11 = 14`. Can you help me?"
)
thread2, run2 = create_thread_and_run("Could you explain linear algebra to me?")
thread3, run3 = create_thread_and_run("I don't like math. What can I do?")

# Pretty printing helper
def pretty_print(messages):
    print("# Messages")
    for m in messages:
        print(f"{m.role}: {m.content[0].text.value}")
        print()

# waiting in a loop
def wait_on_run(run, thread):
    while run.status == "queued" or run.status == "in_progress":
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )
        time.sleep(0.5)
    return run
    

# # Wait for Run1
# run1 = wait_on_run(run1, thread1)
# pretty_print(get_response(thread1))

# # Wait on Run2
# run2 = wait_on_run(run2, thread2)
# pretty_print(get_response(thread2))

# # Wait on Run3
# run2 = wait_on_run(run3, thread3)
# pretty_print(get_response(thread3))

# # Thank our assistant on the Thread 3 :)
# run4 = submit_message(MATH_ASSISTANT_ID, thread3, "Thank you!")
# run4 = wait_on_run(run4, thread3)
# pretty_print(get_response(thread3))

thread, run = create_thread_and_run(
    "Generate the first 20 fibbonaci numbers with code."
)
run = wait_on_run(run, thread)
pretty_print(get_response(thread))
