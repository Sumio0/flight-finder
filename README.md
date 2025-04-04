# ✈️ Flight Finder - Columbia UI Design Midterm Project

This project is part of the **Midterm Assignment** for the course **COMS4170: User Interface Design** at **Columbia University**. It is a fully functional **CRUD flight viewer and editor web application**, with a user-centered interface and a responsive, clean design.

---

## 🔍 Features Overview

### ✅ Full CRUD Functionality
- **Home Page**: shows 3 dynamically loaded popular flights (via JavaScript)
- **Search Bar**: keyword autocomplete and query matching with highlighted results
- **Search Results**: matched items listed with summary, highlight, and click-through
- **Detail Page** (`/view/[id]`): full information for a selected flight, grouped by category
- **Add Flight** (`/add`): form with validation, success message, and reset behavior
- **Edit Flight** (`/edit/[id]`): pre-filled form with discard confirmation modal
- **Data Flow**: form submissions handled via AJAX to `/api/add` and `/api/edit/[id]`

### 🎨 UI & UX Design Principles Applied
- Clear visual **hierarchy** and **grouping** on every page
- Use of **primary / accent / neutral** color palette
- **Accessible**: image alt text, button contrast, clean fonts
- Feedback and form error messages for user input validation
- Responsive layout with mobile-friendly adjustments

---

## ⚙️ Technologies Used

- `Flask` (Python) – backend routing and data processing
- `HTML`, `CSS`, `Bootstrap` – frontend layout and styling
- `JavaScript`, `jQuery` – dynamic interaction and form logic
- `AJAX` – communication between frontend and backend
- `JSON` – in-memory data storage and dynamic loading

---

## 📁 File Structure (Key Files)

```
├── server.py              # Flask backend (routes, API endpoints)
├── flights_data.json      # In-memory JSON storage (mock DB)
├── templates/
│   ├── index.html         # Homepage with featured flights
│   ├── add_flight.html    # Add new flight page
│   ├── edit_flight.html   # Edit flight form
│   ├── search_results.html# Search results display
│   └── view.html          # Detail view page
├── static/
│   ├── script.js          # JS for AJAX, form logic, autocomplete
│   ├── style.css          # Full styling with responsive design
```

---

## 💡 Highlights

- 🔎 **Autocomplete** powered by `/autocomplete` route
- ✏️ **Editing** includes discard confirmation with modal
- 🧠 **Information design** principles inspired by HW1 & HW3
- ✅ **Accessible and responsive** across desktop and mobile

---

## 🎥 Demo Video

[🎬 Watch it on YouTube →](https://www.youtube.com/watch?v=3QULFOBRz5A)

---

## 🧑‍💻 Author

Developed by **Fan Yi** for Columbia UI Design Midterm (Spring 2025)

---

> *This project demonstrates how user interface principles, accessibility, and full-stack engineering can be combined to create highly usable and elegant web tools.*
