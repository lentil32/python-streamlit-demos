import io
import logging
from contextlib import redirect_stdout

import streamlit as st

import pregexy
from pawky import AWKInterpreter

# Configure logging
logging.basicConfig(filename='app.log',
                    filemode='a',
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.ERROR)
logger = logging.getLogger(__name__)

PROJECT_1 = {
    "title": "Pawky - AWK Interpreter in Python",
    "description":
    "**Pawky** is an interpreter for a small subset of the AWK language written in Python",
    "repository": "https://github.com/lentil32/pawky"
}

PROJECT_2 = {
    "title":
    "LC0010. Regular Expression Matching",
    "description":
    "My Python solution for LC0010",
    "repository":
    "https://github.com/lentil32/python-streamlit-demos/blob/main/pregexy/pregexy.py"
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
    if ($3 < 3) {
        defected = 1;
    } else {
        for (i = 1; i <= NF; ++i) {
            if ($i == "NULL") {
                defected = 1;
                break;
            }
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
a1,a2,7
b1,b2,0
c1,c2,11
d1,NULL,24
NILL,e2,1
f1,null,3
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


def run_pregexy():
    st.title(PROJECT_2["title"])
    st.markdown(PROJECT_2["description"], unsafe_allow_html=True)
    st.markdown(f"[Code]({PROJECT_2['repository']})")

    st.header("Text to Compare")
    text = st.text_area(
        "Enter text to compare:",
        "mississippiabbcacbbbbbabcbacaaccbabbacbbbacbcbaacacaaccbaabcbaabcbcbcaccbcaabc",
        height=100)

    st.header("Pattern")
    pattern = st.text_area(
        "Enter pattern:",
        "mis*is*ip*.a*a*.*a*.*a*.b*a*a*.*b*c*b*b*.*ac*.*bc*a*.*a*aa*.*b*.c*.*a*",
        height=100)

    if st.button("Run"):
        # Input Validation
        if not text.strip():
            st.error("Please enter an text to compare.")
            return
        if not pattern.strip():
            st.error("Please enter a pattern.")
            return

        max_text_length = 1000
        max_pattern_length = 1000

        if len(text) > max_text_length:
            st.error(
                f"Text is too long. Maximum allowed length is {max_text_length} characters."
            )
            return
        if len(pattern) > max_pattern_length:
            st.error(
                f"Pattern is too long. Maximum allowed length is {max_pattern_length} characters."
            )
            return

        output = pregexy.is_match(text, pattern)
        st.subheader("Output")
        st.code(output, language='text')


def main():
    st.sidebar.title("lentil32 Dashboard")
    app_mode = st.sidebar.radio("Demos",
                                [PROJECT_1["title"], PROJECT_2["title"]])

    if app_mode == PROJECT_1["title"]:
        run_pawky()
    elif app_mode == PROJECT_2["title"]:
        run_pregexy()
    else:
        st.error("Unknown option selected.")


if __name__ == '__main__':
    main()
