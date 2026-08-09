# Frontend Architecture

> **Project:** AI Concierge – Personalized AI Assistant

> **Document Version:** 1.0

> **Status:** Draft

---

# 1. Purpose

This document describes the architecture of the AI Concierge frontend application.

It explains:

- Project structure
- Component hierarchy
- Routing
- State management
- API communication
- Authentication flow
- UI organization
- Performance considerations

The frontend is designed using modern React best practices to ensure scalability, maintainability, and a clean separation of concerns.

---

# 2. Technology Stack

| Technology | Purpose |
|------------|---------|
| React | UI Framework |
| TypeScript | Static typing |
| Tailwind CSS | Styling |
| Shadcn/UI | Reusable UI components |
| React Router | Navigation |
| TanStack Query | API data fetching and caching |
| Axios | HTTP client |
| React Hook Form | Forms |
| Zod | Form validation |
| Lucide React | Icons |
| React Markdown | Render AI responses |

---

# 3. Frontend Design Goals

The frontend architecture is designed to be:

- Modular
- Reusable
- Responsive
- Accessible
- Fast
- Easy to maintain
- Easy to test

---

# 4. High-Level Architecture

```
Browser
    │
    ▼
React Application
    │
    ├───────────────┐
    ▼               ▼
Pages          Shared Components
    │               │
    ▼               ▼
Feature Modules    UI Components
    │
    ▼
API Layer
    │
    ▼
FastAPI Backend
```

---

# 5. Folder Structure

```
src/

│

├── app/

├── assets/

├── components/

├── features/

├── hooks/

├── layouts/

├── lib/

├── pages/

├── routes/

├── services/

├── store/

├── styles/

├── types/

├── utils/

└── main.tsx
```

---

# 6. Folder Responsibilities

## app/

Application configuration.

Examples

- Providers
- Theme
- Query Client
- Router

---

## assets/

Static resources.

Examples

- Images
- Logos
- Fonts
- Icons

---

## components/

Reusable components.

Examples

- Buttons
- Cards
- Dialogs
- Navbar
- Sidebar

These components should not contain business logic.

---

## features/

Feature-specific components.

Examples

```
chat/

documents/

planner/

memory/

history/

settings/
```

Each feature owns:

- UI
- Hooks
- API calls
- Types

---

## hooks/

Custom React hooks.

Examples

```
useChat()

useMemory()

useUpload()

useUser()

usePlanner()
```

---

## layouts/

Application layouts.

Examples

```
DashboardLayout

AuthLayout

LandingLayout
```

---

## pages/

Page-level components.

Examples

```
Dashboard

Chat

Documents

History

Planner

Settings

Login

Register
```

---

## routes/

Application routing.

Contains:

- Protected Routes
- Public Routes
- Route definitions

---

## services/

API communication.

Examples

```
auth.service.ts

chat.service.ts

memory.service.ts

document.service.ts
```

Only this layer communicates with the backend.

---

## store/

Global state.

Stores:

- User
- Theme
- Authentication
- Preferences

Server state should primarily be managed using TanStack Query.

---

## utils/

Helper functions.

Examples

- Date formatting
- Text formatting
- Language utilities

---

## types/

Shared TypeScript interfaces.

Examples

```
User

Message

Conversation

Document

Memory
```

---

# 7. Routing Architecture

```
/

↓

Landing

↓

/login

/register

/dashboard

/chat

/documents

/planner

/history

/memory

/settings
```

Protected routes require authentication.

---

# 8. Layout Structure

```
Dashboard Layout

┌──────────────────────────────┐

Sidebar

Navbar

Main Content

Footer (optional)

└──────────────────────────────┘
```

---

# 9. Sidebar Navigation

```
🏠 Dashboard

💬 Chat

📄 Documents

🧠 Memory

📅 Planner

🕓 History

⚙ Settings

🚪 Logout
```

---

# 10. Component Hierarchy

```
App

↓

Router

↓

Dashboard Layout

↓

Chat Page

↓

Chat Window

↓

Message List

↓

Message Bubble

↓

Markdown Renderer
```

---

# 11. State Management

## Local State

Used for:

- Form input
- Dialog visibility
- Selected document

Managed using React hooks.

---

## Global State

Stores:

- User
- Authentication
- Theme
- Language preference

---

## Server State

Managed using TanStack Query.

Examples

- Conversations
- Documents
- Memory
- Planner

Benefits:

- Automatic caching
- Background refetching
- Loading states
- Retry logic

---

# 12. API Layer

All backend communication goes through service classes.

Example:

```
Chat Page

↓

chatService.sendMessage()

↓

Axios

↓

FastAPI
```

Components never call APIs directly.

---

# 13. Authentication Flow

```
Login Page

↓

Submit Credentials

↓

Auth API

↓

JWT Token

↓

Store Token

↓

Redirect Dashboard
```

Protected routes validate authentication before rendering.

---

# 14. Chat Module

Main components:

```
Chat Page

↓

Chat Window

↓

Message List

↓

Message Bubble

↓

Input Box

↓

Suggested Prompts
```

---

# 15. Document Module

```
Document Page

↓

Upload Area

↓

Document List

↓

Search

↓

Preview

↓

Delete
```

---

# 16. Memory Module

```
Memory Page

↓

Memory Cards

↓

Search

↓

Edit

↓

Delete
```

---

# 17. Planner Module

```
Planner

↓

Today's Tasks

↓

Weekly Planner

↓

Goal Tracker
```

---

# 18. Settings Module

```
Settings

↓

Profile

Language

Theme

Notifications

Security
```

---

# 19. Error Handling

The frontend should gracefully handle:

- Network failures
- Authentication expiration
- Upload failures
- Empty search results
- API timeouts

Users should receive friendly error messages instead of technical exceptions.

---

# 20. Loading States

Examples:

- Skeleton loaders
- Upload progress bars
- Typing indicators
- Spinner during authentication

Loading feedback improves perceived responsiveness.

---

# 21. Responsive Design

### Desktop

- Permanent sidebar
- Wide chat layout

### Tablet

- Collapsible sidebar
- Adaptive grids

### Mobile

- Bottom navigation
- Full-screen chat
- Drawer menu

---

# 22. Accessibility

The frontend should support:

- Keyboard navigation
- Screen readers
- High-contrast themes
- Semantic HTML
- ARIA labels
- Visible focus indicators

---

# 23. Performance Optimization

The application should optimize performance by:

- Lazy loading pages
- Code splitting
- Image optimization
- Memoizing expensive components
- Virtualizing long conversation lists
- Debouncing search inputs
- Efficient caching with TanStack Query

---

# 24. Frontend Security

Security considerations include:

- Sanitizing rendered Markdown
- Secure JWT storage strategy
- Preventing XSS attacks
- Avoiding exposure of sensitive configuration
- Validating user input before submission

---

# 25. Future Enhancements

Future frontend capabilities may include:

- Voice interface
- Drag-and-drop document upload
- Dark mode customization
- Offline support (Progressive Web App)
- Mobile application
- Collaborative workspaces

---

# 26. Summary

The frontend architecture emphasizes modularity, reusability, and maintainability. By separating presentation, state management, routing, and API communication, the application remains easy to extend as new features are added. This structure supports both rapid MVP development and future growth into a production-grade AI platform.
