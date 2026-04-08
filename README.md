# 🎓 Travail - Advanced Placement Management System

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)
![Status](https://img.shields.io/badge/Status-100%25_Complete-success?style=for-the-badge)

**Travail** is a robust, role-based placement portal designed to automate university recruitment workflows. It provides a seamless interface for Administrators to vet companies, Companies to manage job drives, and Students to track their career opportunities.

---

## 📌 Table of Contents
- [System Architecture](#-system-architecture)
- [Module Breakdowns](#-module-breakdowns)
- [Security Implementation](#-security-implementation)
- [Installation Guide](#-installation-guide)
- [Database Schema](#-database-schema)

---

## 🏛 System Architecture

The project follows a **Modular Design** using Flask Blueprints to separate concerns between different user roles.

| Role | Key Responsibilities |
| :--- | :--- |
| **Admin** | Verification of companies/drives, system-wide analytics, user blacklisting. |
| **Company** | Posting drives, shortlisting candidates, profile management. |
| **Student** | Applying for drives, real-time status tracking, resume management. |

---

## 🚀 Module Breakdowns

### 🛡 Admin Features
- **Global Dashboard:** Aggregated data of all portal activities.
- **Vetting Process:** Manual approval switch for new company registrations.
- **Search Engine:** Filter students/companies by UID, Name, or Contact.

### 💼 Company Features
- **Drive CRUD:** Complete Create, Read, Update, and Delete lifecycle for placement drives.
- **ATS (Applicant Tracking System):** Manage student applications and download PDF resumes.

### 🎓 Student Features
- **Smart Filter:** Only see drives that are **Approved** and **Active** (Deadline not passed).
- **Application History:** Visual tracking of "Applied", "Shortlisted", and "Selected" statuses.

---

## 🔐 Security Implementation

> [!IMPORTANT]
> This project implements several industry-standard security practices for academic evaluation.

- **Role-Based Access Control (RBAC):** Custom Python decorators (`@admin_required`, `@student_required`) protect sensitive routes from URL tampering.
- **Secure File Handling:** Resumes are processed via `werkzeug.secure_filename` to prevent path traversal attacks.
- **Data Integrity:** Foreign Key constraints ensure that deleting a company or drive properly handles associated applications.

---

## 🏗 Database Schema
The system uses a relational SQLite database. 

**Core Entities:**
- `Users`: Central authentication and role flag.
- `Company`: Profile and approval status.
- `Drive`: Placement details and deadlines.
- `Application`: Relationship table linking students and drives.

---

## ⚙️ Installation Guide

1. **Clone the Project**
   ```bash
   git clone [https://github.com/sunnykbharti/placement-portal.git](https://github.com/sunnykbharti/placement-portal.git)
   ```
2. **Configure Environment**
  ```bash
  python -m venv venv
  venv\Scripts\activate
  pip install -r requirements.txt
  ```
3. **Launch**
  ```bash
  python app.py
  ```
