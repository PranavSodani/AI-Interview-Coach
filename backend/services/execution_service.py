import subprocess
import tempfile
import os


def execute_code(
    code: str,
    function_name: str,
    test_cases: list
):

    results = []

    try:

        for test_case in test_cases:

            function_call = (
                f"\nresult = "
                f"{function_name}"
                f"(*{test_case.input_data})\n"
                f"print(result)\n"
            )

            complete_code = code + "\n" + function_call

            with tempfile.NamedTemporaryFile(
                mode="w",
                suffix=".py",
                delete=False
            ) as temp_run_file:

                temp_run_file.write(complete_code)

                temp_run_path = temp_run_file.name

            result = subprocess.run(
                [
                    "docker",
                    "run",
                    "--rm",
                    "-i",
                    "ai-code-sandbox"
                ],
                input=complete_code,
                capture_output=True,
                text=True,
                timeout=5
            )

            error_message = result.stderr.strip()

            actual_output = result.stdout.strip()

            passed = (
                actual_output ==
                str(test_case.expected_output).strip()
            )

            results.append({
                "input_data": test_case.input_data,
                "expected_output": test_case.expected_output,
                "actual_output": actual_output,
                "passed": passed,
                "error": (
                    error_message
                    if error_message
                    else None
                )
            })

            os.remove(temp_run_path)

        all_passed = all(
            result["passed"]
            for result in results
        )

        return {
            "results": results,
            "all_passed": all_passed
        }

    except subprocess.TimeoutExpired:

        return {
            "results": [],
            "all_passed": False,
            "error": "Code execution timed out"
        }

    except Exception as e:

        return {
            "results": [],
            "all_passed": False,
            "error": str(e)
        }