# OnPrem.LLM

<!-- WARNING: THIS FILE WAS AUTOGENERATED! DO NOT EDIT! -->

> A tool for running large language models on-premises using non-public
> data

**OnPrem.LLM** is a simple Python package that makes it easier to run
large language models (LLMs) on your own machines using non-public data
(possibly behind corporate firewalls). Inspired by the
[privateGPT](https://github.com/imartinez/privateGPT) GitHub repo and
Simon Willison’s [LLM](https://pypi.org/project/llm/) command-line
utility, **OnPrem.LLM** is intended to help integrate local LLMs into
practical applications.

The full documentation is [here](https://amaiya.github.io/onprem/).

A Google Colab demo of installing and using **OnPrem.LLM** is
[here](https://colab.research.google.com/drive/1LVeacsQ9dmE1BVzwR3eTLukpeRIMmUqi?usp=sharing).

## Install

Once you have [installed
PyTorch](https://pytorch.org/get-started/locally/), you can install
**OnPrem.LLM** with:

``` sh
pip install onprem
```

For fast GPU-accelerated inference, see [additional instructions
below](https://amaiya.github.io/onprem/#speeding-up-inference-using-a-gpu).

## How to Use

### Setup

``` python
from onprem import LLM

llm = LLM()
```

By default, a 7B-parameter model is downloaded and used. If
`use_larger=True`, a 13B-parameter is used. You can also supply the URL
to an LLM of your choosing to
[`LLM`](https://amaiya.github.io/onprem/core.html#llm) (see the [code
generation section
below](https://amaiya.github.io/onprem/#text-to-code-generation) for an
example). As of v0.0.20, **OnPrem.LLM** supports the newer GGUF format.

### Send Prompts to the LLM to Solve Problems

This is an example of few-shot prompting, where we provide an example of
what we want the LLM to do.

``` python
prompt = """Extract the names of people in the supplied sentences. Here is an example:
Sentence: James Gandolfini and Paul Newman were great actors.
People:
James Gandolfini, Paul Newman
Sentence:
I like Cillian Murphy's acting. Florence Pugh is great, too.
People:"""

saved_output = llm.prompt(prompt)
```


    Cillian Murphy, Florence Pugh

Additional prompt examples are [shown
here](https://amaiya.github.io/onprem/examples.html).

### Talk to Your Documents

Answers are generated from the content of your documents (i.e.,
[retrieval augmented generation](https://arxiv.org/abs/2005.11401) or
RAG). Here, we will supply `use_larger=True` to use the larger default
model better suited to this use case in addition to using [GPU
offloading](https://amaiya.github.io/onprem/#speeding-up-inference-using-a-gpu)
to speed up answer generation.

``` python
from onprem import LLM

llm = LLM(use_larger=True, n_gpu_layers=35)
```

#### Step 1: Ingest the Documents into a Vector Database

``` python
llm.ingest('./sample_data')
```

    Creating new vectorstore at /home/amaiya/onprem_data/vectordb
    Loading documents from ./sample_data
    Loaded 12 new documents from ./sample_data
    Split into 153 chunks of text (max. 500 chars each)
    Creating embeddings. May take some minutes...
    Ingestion complete! You can now query your documents using the LLM.ask method

    Loading new documents: 100%|██████████████████████| 3/3 [00:00<00:00, 25.52it/s]

#### Step 2: Answer Questions About the Documents

``` python
question = """What is  ktrain?""" 
answer, docs = llm.ask(question)
```

     ktrain is a low-code platform designed to facilitate the full machine learning workflow, from preprocessing inputs to training, tuning, troubleshooting, and applying models. It focuses on automating other aspects of the ML workflow in order to augment and complement human engineers rather than replacing them. Inspired by fastai and ludwig, ktrain is intended to democratize machine learning for beginners and domain experts with minimal programming or data science experience.

The sources used by the model to generate the answer are stored in
`docs`:

``` python
print('\nSources:\n')
for i, document in enumerate(docs):
    print(f"\n{i+1}.> " + document.metadata["source"] + ":")
    print(document.page_content)
```


    Sources:


    1.> ./sample_data/ktrain_paper.pdf:
    lection (He et al., 2019). By contrast, ktrain places less emphasis on this aspect of au-
    tomation and instead focuses on either partially or fully automating other aspects of the
    machine learning (ML) workﬂow. For these reasons, ktrain is less of a traditional Au-
    2

    2.> ./sample_data/ktrain_paper.pdf:
    possible, ktrain automates (either algorithmically or through setting well-performing de-
    faults), but also allows users to make choices that best ﬁt their unique application require-
    ments. In this way, ktrain uses automation to augment and complement human engineers
    rather than attempting to entirely replace them. In doing so, the strengths of both are
    better exploited. Following inspiration from a blog post1 by Rachel Thomas of fast.ai

    3.> ./sample_data/ktrain_paper.pdf:
    with custom models and data formats, as well.
    Inspired by other low-code (and no-
    code) open-source ML libraries such as fastai (Howard and Gugger, 2020) and ludwig
    (Molino et al., 2019), ktrain is intended to help further democratize machine learning by
    enabling beginners and domain experts with minimal programming or data science experi-
    4. http://archive.ics.uci.edu/ml/datasets/Twenty+Newsgroups
    6

    4.> ./sample_data/ktrain_paper.pdf:
    ktrain: A Low-Code Library for Augmented Machine Learning
    toML platform and more of what might be called a “low-code” ML platform. Through
    automation or semi-automation, ktrain facilitates the full machine learning workﬂow from
    curating and preprocessing inputs (i.e., ground-truth-labeled training data) to training,
    tuning, troubleshooting, and applying models. In this way, ktrain is well-suited for domain
    experts who may have less experience with machine learning and software coding. Where

### Text to Code Generation

We’ll use the CodeUp LLM by supplying the URL and employing the
particular prompt format this model expects.

``` python
from onprem import LLM
url = 'https://huggingface.co/TheBloke/CodeUp-Llama-2-13B-Chat-HF-GGUF/resolve/main/codeup-llama-2-13b-chat-hf.Q4_K_M.gguf'
llm = LLM(url, n_gpu_layers=43) # see below for GPU information
```

Setup the prompt based on what [this model
expects](https://huggingface.co/TheBloke/CodeUp-Llama-2-13B-Chat-HF-GGUF#prompt-template-alpaca)
(this is important):

``` python
template = """
Below is an instruction that describes a task. Write a response that appropriately completes the request.

### Instruction:
{prompt}

### Response:"""
```

``` python
answer = llm.prompt('Write Python code to validate an email address.', prompt_template=template)
```


    Here is an example of Python code that can be used to validate an email address:
    ```
    import re

    def validate_email(email):
        # Use a regular expression to check if the email address is in the correct format
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if re.match(pattern, email):
            return True
        else:
            return False

    # Test the validate_email function with different inputs
    print("Email address is valid:", validate_email("example@example.com"))  # Should print "True"
    print("Email address is invalid:", validate_email("example@"))  # Should print "False"
    print("Email address is invalid:", validate_email("example.com"))  # Should print "False"
    ```
    The code defines a function `validate_email` that takes an email address as input and uses a regular expression to check if the email address is in the correct format. The regular expression checks for an email address that consists of one or more letters, numbers, periods, hyphens, or underscores followed by the `@` symbol, followed by one or more letters, periods, hyphens, or underscores followed by a `.` and two to three letters.
    The function returns `True` if the email address is valid, and `False` otherwise. The code also includes some test examples to demonstrate how to use the function.

Let’s try out the code generated above.

``` python
import re
def validate_email(email):
    # Use a regular expression to check if the email address is in the correct format
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(pattern, email):
        return True
    else:
        return False
print(validate_email('sam@@openai.com')) # bad email address
print(validate_email('sam@openai'))      # bad email address
print(validate_email('sam@openai.com'))  # good email address
```

    False
    False
    True

The generated code may sometimes need editing, but this one worked
out-of-the-box.

## Built-In Web App

**OnPrem.LLM** includes a built-in Web app to access the LLM. To start
it, run the following command after installation:

``` shell
onprem --port 8000
```

Then, enter `localhost:8000` (or `<domain_name>:8000` if running on
remote server) in a Web browser to access the application:

<img src="https://raw.githubusercontent.com/amaiya/onprem/master/onprem_screenshot.png" border="1" alt="screenshot" width="800"/>

For more information, [see the corresponding
documentation](https://amaiya.github.io/onprem/webapp.html).

## Speeding Up Inference Using a GPU

The above example employed the use of a CPU.  
If you have a GPU (even an older one with less VRAM), you can speed up
responses.

#### Step 1: Install `llama-cpp-python` with CUBLAS support

``` shell
CMAKE_ARGS="-DLLAMA_CUBLAS=on" FORCE_CMAKE=1 pip install --upgrade --force-reinstall llama-cpp-python==0.1.69 --no-cache-dir
```

It is important to use the specific version shown above due to library
incompatibilities.

#### Step 2: Use the `n_gpu_layers` argument with [`LLM`](https://amaiya.github.io/onprem/core.html#llm)

``` python
llm = LLM(n_gpu_layers=35)
```

The value for `n_gpu_layers` depends on your GPU memory and the model
you’re using (e.g., max of 35 for default 7B model). You can reduce the
value if you get an error (e.g., `CUDA OOM`) or you observe the model
stalling in the middle of a response.

With the steps above, calls to methods like `llm.prompt` will offload
computation to your GPU and speed up responses from the LLM.

## FAQ

1.  **How do I use other models with OnPrem.LLM?**

    > You can supply the URL to other models to the `LLM` constructor,
    > as we did above in the code generation example.

    > As of v0.0.20, we support models in GGUF format, which supersedes
    > the older GGML format. You can find llama.cpp-supported models
    > with `GGUF` in the file name on
    > [huggingface.co](https://huggingface.co/models?sort=trending&search=gguf).

2.  **I’m behind a corporate firewall and am receiving an SSL error when
    trying to download the model?**

    > Try this:
    >
    > ``` python
    > from onprem import LLM
    > LLM.download_model(url, ssl_verify=False)
    > ```

3.  **How do I use this on a machine with no internet access?**

    > Use the `LLM.download_model` method to download the model files to
    > `<your_home_directory>/onprem_data` and transfer them to the same
    > location on the air-gapped machine.

    > For the `ingest` and `ask` methods, you will need to also download
    > and transfer the embedding model files:
    >
    > ``` python
    > from sentence_transformers import SentenceTransformer
    > model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    > model.save('/some/folder')
    > ```

    > Copy the `some/folder` folder to the air-gapped machine and supply
    > the path to `LLM` via the `embedding_model_name` parameter.

4.  **When installing `onprem`, I’m getting errors related to
    `llama-cpp-python` on Windows/Mac/Linux?**

    > For **Linux** systems like Ubuntu, try this:
    > `sudo apt-get install build-essential g++ clang`. Other tips are
    > [here](https://github.com/oobabooga/text-generation-webui/issues/1534).

    > For **Windows** systems, either use [Windows Subsystem for Linux
    > (WSL)](https://learn.microsoft.com/en-us/windows/wsl/install) or
    > install [Microsoft Visual Studio build
    > tools](https://visualstudio.microsoft.com/vs/older-downloads/) and
    > ensure the selections shown in [this
    > post](https://github.com/imartinez/privateGPT/issues/445#issuecomment-1561343405)
    > are installed. WSL is recommended.

    > For **Macs**, try following [these
    > tips](https://github.com/imartinez/privateGPT/issues/445#issuecomment-1563333950).

    > If you still have problems, there are various other tips for each
    > of the above OSes in [this privateGPT repo
    > thread](https://github.com/imartinez/privateGPT/issues/445). Of
    > course, you can also [easily
    > use](https://colab.research.google.com/drive/1LVeacsQ9dmE1BVzwR3eTLukpeRIMmUqi?usp=sharing)
    > **OnPrem.LLM** on Google Colab.

5.  **`LlamaCpp` is failing to load my model from the model path on
    Google Colab.**

    > For reasons that are unclear, newer versions of `llama-cpp-python`
    > fail to load models on Google Colab unless you supply
    > `verbose=True` to the `LLM` constructor.
