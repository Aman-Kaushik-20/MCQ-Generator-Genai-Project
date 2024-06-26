from setuptools import find_packages, setup





setup(
    name = 'mcqgenerator',
    version = '0.0.1',
    author = 'Aman Kaushik',
    author_email = "amankaushik20112001@gmail.com",
    packages  = find_packages(),
    install_requires = ["openai","lanchain","streamlit","python-dotenv","PyPDF2"]
)