docker run --name pgvector-container -e POSTGRES_USER=langchain -e POSTGRES_PASSWORD=langchain -e POSTGRES_DB=langchain -p 6024:5432 -d pgvector/pgvector:pg16


response.data.payload.output


Sample Questions for User Interaction with an Insurance Agent:
"Can you give me the claim status? My claim ID is [ClaimID]."
"Can you tell me about my insurance policy?"
"Can you provide detailed information regarding my insurance policy?"

uvicorn main:app --reload
