# AI Concierge - Database Design

## Database

PostgreSQL

## Users Table

Fields:

* id
* username
* email
* password_hash
* created_at

## UserPreferences Table

Fields:

* id
* user_id
* preferred_response_style
* interests
* budget
* food_preferences

## Sessions Table

Fields:

* id
* user_id
* created_at

## Conversations Table

Fields:

* id
* session_id
* title
* created_at

## Messages Table

Fields:

* id
* conversation_id
* role
* content
* timestamp

## Documents Table

Fields:

* id
* user_id
* filename
* upload_date

## DocumentChunks Table

Fields:

* id
* document_id
* chunk_index
* chunk_text
* embedding_id

## AuditLogs Table

Fields:

* id
* user_id
* action
* timestamp

## Relationships

User
→ Sessions

User
→ Preferences

Session
→ Conversations

Conversation
→ Messages

User
→ Documents

Document
→ Chunks

## Future Tables

* Feedback
* Recommendations
* Tool Usage Analytics
* Agent Traces
