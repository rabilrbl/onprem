# Changes

Most recent releases are shown at the top. Each release shows:

- **New**: New classes, methods, functions, etc
- **Changed**: Additional parameters, changes to inputs or outputs, etc
- **Fixed**: Bug fixes that don't change documented behaviour

## 0.0.28 (development)

### new:
- N/A

### changed
- N/A

### fixed:
- N/A


## 0.0.27 (2023-09-30)

### new:
- N/A

### changed
- Remove pin for `llama-cpp-python` so latest is always used (#33)

### fixed:
- N/A


## 0.0.26 (2023-09-27)

### new:
- N/A

### changed
- Include `prompt_template` variable in YAML (#32)

### fixed:
- N/A



## 0.0.25 (2023-09-27)

### new:
- N/A

### changed
- **Breaking Change**: The `LLM.ask` method now returns a dictionary with keys: `answer`, `source_documents`, and `question` (#31)

### fixed:
- N/A


## 0.0.24 (2023-09-26)

### new:
- N/A

### changed
- Added `rag_text_path` and `verbose` to default `webapp.yml`.

### fixed:
- Moving `load_llm` to constructor seems to prevent model loading issues in `Llamacpp` (#30)


## 0.0.23 (2023-09-25)

### new:
- N/A

### changed
- round scores in web app to 3 decimal places (#29)

### fixed:
- N/A


## 0.0.22 (2023-09-24)

### new:
- attempt to auto-create symlinks for serving source documents

### changed
- N/A

### fixed:
- N/A


## 0.0.21 (2023-09-22)

### new:
- Support for hyperlinks to sources in RAG screen of  Web app (#28)

### changed
- N/A

### fixed:
- `LLM.ingest` converts relative paths to absolute paths during ingestion


## 0.0.20 (2023-09-22)

### new:
- Support for `GGUF` format as the default LLM format. (#1)

### changed
- All default models have been changed to `GGUF` models.
- updated pin for `llama-cpp-python` to support GGUF format.

### fixed:
- Misc adjustments and bug fixes for built-in Web app


## 0.0.19 (2023-09-21)

### new:
- Built-in Web app for both RAG and general prompting

### changed
- **Possible Breaking Change**: Support for `score_threshold` in `LLM.ask` and `LLM.chat` (#26)
- Use `CallbackManager` (#24)

### fixed:
- N/A



## 0.0.18 (2023-09-18)

### new:
- N/A

### changed
- `LLM.chat` now includes `source_documents` in output (#23)

### fixed:
- N/A


## 0.0.17 (2023-09-17)

### new:
- The `LLM.chat` method supports question-answering with conversational memory. (#20)

### changed
- `LLM` now accepts a `callbacks` parameter for custom callbacks. (#21)
- added additional examples

### fixed:
- N/A


## 0.0.16 (2023-09-12)

### new:
- Support for prompt templates in `ask` (#17)

### changed
- Added `LLM.load_qa` method

### fixed:
- batchify input to `Chroma` (#18)


## 0.0.15 (2023-09-11)

### new:
- N/A

### changed
- N/A

### fixed:
- pass `embedding_model_kwargs` and `embedding_encode_kwargs` to `HuggingFaceEmbeddings` (#16)


## 0.0.14 (2023-09-11)

### new:
- N/A

### changed
- Added `Ingester.get_embeddings` method to access instance of `HuggingFaceEmbeddings`
- Added `chunk_size` and `chunk_overlap` parameters to `Ingester.ingest` and `LLM.ingest` (#13)

### fixed:
- Check to ensure `source_directory` is a folder in `LLM.ingest` (#15)


## 0.0.13 (2023-09-10)

### new:
- N/A

### changed
- Accept extra `kwargs` and supply them to `langchain.llms.Llamacpp` (#12)
- Add optional argument to specify custom path to vector DB (#11)

### fixed:
- N/A


## 0.0.12 (2023-09-09)

### new:
- N/A

### changed
- Add optional argument to specify custom path to download LLM (#5), thanks to @rabilrbl

### fixed:
- Fixed capitalization in download confirmation (#9), thanks to @rabilrbl
- Insert [dummy replacement](https://stackoverflow.com/questions/74918614/error-importing-seaborn-module-attributeerror/76760670#76760670) of decorator into numpy



## 0.0.11 (2023-09-07)

### new:
- N/A

### changed
- Print `persist_directory` when creating new vector store
- Revert `numpy` pin

### fixed:
- N/A



## 0.0.10 (2023-09-07)

### new:
- N/A

### changed
- Pin to `numpy==1.23.3` due to `_no_nep50` error in some environments

### fixed:
- N/A


## 0.0.9 (2023-09-06)

- Last release without CHANGELOG updates

