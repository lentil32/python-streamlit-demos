import io
import logging
from contextlib import redirect_stdout

import streamlit as st

from pawky import AWKInterpreter

# Configure logging
logging.basicConfig(filename='app.log',
                    filemode='a',
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.ERROR)
logger = logging.getLogger(__name__)

PROJECT_1 = {
    "title": "Pawky - AWK Interpreter in Python",
    "description": "**Pawky** is an AWK interpreter written in Python.",
    "repository": "https://github.com/lentil32/pawky"
}


def run_pawky():
    st.title(PROJECT_1["title"])
    st.markdown(PROJECT_1["description"], unsafe_allow_html=True)
    st.markdown(f"[GitHub Repository]({PROJECT_1['repository']})")

    st.header("AWK Script")
    awk_script = st.text_area("Enter AWK script:",
                              """\
BEGIN {
    FS = ",";
}

{
    defected = 0;
    for (i = 1; i <= NF; ++i) {
        if ($i == "NULL") {
            defected = 1;
            break;
        }
    }
    if (!defected)
        print $0;
}
    """,
                              height=400)

    st.header("Input Data")
    input_data = st.text_area("Enter input data:",
                              """\
a1,a2,a3
b1,b2,b3
c1,c2,c3
d1,NULL,d3
NILL,e2,e3
f1,f2,null
    """,
                              height=250)

    if st.button("Run Interpreter"):
        # Input Validation
        if not awk_script.strip():
            st.error("Please enter an AWK script.")
            return
        if not input_data.strip():
            st.error("Please enter input data.")
            return

        max_script_length = 5000
        max_input_length = 10000

        if len(awk_script) > max_script_length:
            st.error(
                f"AWK script is too long. Maximum allowed length is {max_script_length} characters."
            )
            return
        if len(input_data) > max_input_length:
            st.error(
                f"Input data is too long. Maximum allowed length is {max_input_length} characters."
            )
            return

        # Capture the output of the interpreter
        buffer = io.StringIO()
        try:
            with redirect_stdout(buffer):
                interpreter = AWKInterpreter(awk_script)
                interpreter.set_input(input_data)
                interpreter.run()
        except Exception:
            logger.error("Error running AWK interpreter", exc_info=True)
            st.error(
                "An error occurred while executing the AWK script. Please check your script and input data."
            )
            return

        output = buffer.getvalue()
        if output:
            st.subheader("Output")
            st.code(output, language='text')
        else:
            st.info("No output generated.")


def main():
    st.sidebar.title("lentil32 Dashboard")
    app_mode = st.sidebar.radio("Demos", [PROJECT_1["title"]])

    if app_mode == PROJECT_1["title"]:
        run_pawky()
    else:
        st.error("Unknown option selected.")


if __name__ == '__main__':
    main()
