# mini-dify
mini project about how  a dify was born

## what is this
This is a small project called mini-dify which build from zero to one function. It would improves me a lot. I always would like using a real engineering project for me to study something i interested in.

## why you build this 
The core reason I build this is to get a summer backend internship of Dify, which is really important for me. 

## The core structure
frontend : Vue3
backend: python + Flask (Which is dify offical repo always used)
sql: PostgresSQL + Redis
other tool: Git
ok that's it 

## The implementation.
1. ingest_document(file) -> The Entry Point
This function handles the raw physical upload.

What it does: It receives the file, generates a unique document_id, saves the file to a local storage/ folder, and creates a record in your PostgreSQL table with the status PENDING.

ByteDance Challenge: Instead of just saving to disk, try to generate a presigned URL or simulate an "Object Storage" (like S3/OSS) upload.

2. trigger_pipeline(document_id) -> The Orchestrator
This is the bridge between your API and your Worker.

What it does: It calls process_document.delay(document_id).

The "Wise" Detail: You only pass the ID, not the whole file. This keeps your Redis queue lightweight.

3. process_document_task(document_id) -> The Worker (The "Brain")
This is where you spend 80% of your effort. It should be a Celery task that executes these steps:

Parse: Read the .txt or .pdf and extract the text.

Chunk: Don't just save the whole text. Split it into 500-word "chunks." (In Dify, this is the dataset_process_rules logic).

Embed (Simulated): In a real app, you’d call OpenAI/HuggingFace. For now, just simulate a 2-second delay to represent the "work."

Load: Save these chunks into a new database table called document_segments.

4. query_knowledge(user_query) -> The Retrieval
This is the function that makes the knowledge "useful."

What it does: It looks through your document_segments and finds the most relevant text.

Simplified Logic: For your version, you can just use a simple SQL LIKE %query% or "Keyword Search" before you move on to complex Vector Searches.


```
/mini-dify
├── /api          # Flask routes (ingest_document, query_knowledge)
├── /core         # The logic (parsing, chunking, embedding)
├── /tasks        # Celery task definitions (process_document_task)
├── /models       # SQLAlchemy Database models (Document, Segment)
├── docker-compose.yaml
└── requirements.txt
```