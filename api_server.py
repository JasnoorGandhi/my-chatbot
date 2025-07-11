from fastapi import FastAPI
from pydantic import BaseModel
from db_connect import get_engine
from schema_embed import retrieve_relevant_schema
from sql_generator import generate_sql_query, parse_sql_query, execute_sql_query, summarize_results

app = FastAPI()
engine = get_engine()

class ChatRequest(BaseModel):
    question: str

class ChatResponse(BaseModel):
    answer: str
    sql_query: str = None

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    prompt = request.question
    relevant_schemas = retrieve_relevant_schema(prompt)
    schema_text = "\n".join(relevant_schemas)
    sql_query = generate_sql_query(schema_text, prompt)
    parsed_query, is_valid = parse_sql_query(sql_query, engine)
    if not is_valid:
        return ChatResponse(answer=f"SQL Query Error: {parsed_query}", sql_query=sql_query)
    result, success = execute_sql_query(parsed_query, engine)
    if success:
        summary = summarize_results(prompt, result["columns"], result["rows"])
        # Robust extraction of content
        if isinstance(summary, dict) and "content" in summary:
            answer = summary["content"]
        elif hasattr(summary, "content"):
            answer = summary.content
        else:
            answer = str(summary)
        return ChatResponse(answer=answer, sql_query=sql_query)
    else:
        return ChatResponse(answer=f"Execution Error: {result}", sql_query=sql_query)

# Optional: Add CORS middleware if needed for cross-origin requests
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to restrict allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
