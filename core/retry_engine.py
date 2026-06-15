import time

def retry_loop(func, retries=3):

    history = []

    for i in range(retries):

        try:

            result = func()

            history.append({
                "attempt": i + 1,
                "success": True
            })

            return {
                "success": True,
                "history": history,
                "result": result
            }

        except Exception as e:

            history.append({
                "attempt": i + 1,
                "success": False,
                "error": str(e)
            })

            time.sleep(2)

    return {
        "success": False,
        "history": history
    }
