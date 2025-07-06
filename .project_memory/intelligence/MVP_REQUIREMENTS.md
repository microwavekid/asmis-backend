# MVP Requirements Document

**Date:** 2025-07-08
**Status:** Draft for Stakeholder Review

---

## Overview
This document consolidates all features, user stories, and acceptance criteria for the ASMIS MVP. It is intended to ensure alignment among all stakeholders and serve as the single source of truth for MVP delivery.

---

## Feature Categories & Requirements

### 1. Security & Access Control

#### Feature: Multi-Tenant Access Control
- **User Story:**
  - As an organization admin, I want all my company's data to be isolated from other customers, so that we can ensure privacy and compliance.
- **Acceptance Criteria:**
  - All data models include a tenant_id field.
  - API endpoints enforce tenant isolation and ownership checks.
  - Users can only access data belonging to their tenant.
  - Attempts to access data from another tenant are denied and logged.

#### Feature: User Authentication
- **User Story:**
  - As a new user, I want to sign up and log in with email and password, so that I can securely access my account.
- **Acceptance Criteria:**
  - Users can register with email and password.
  - Passwords are securely hashed and never stored in plaintext.
  - Users can log in and receive a session/token.
  - Invalid login attempts are handled securely.

---

### 2. Core Platform

#### Feature: Core Architecture & Database Schema
- **User Story:**
  - As a developer, I want a robust backend and frontend foundation, so that features can be built and maintained efficiently.
- **Acceptance Criteria:**
  - Project structure and environment configuration are established.
  - Database schema includes users, accounts, deals, and other core entities.
  - Migrations are in place and tested.

#### Feature: Deal Management API
- **User Story:**
  - As a user, I want to create, view, update, and list deals, so that I can manage my sales pipeline.
- **Acceptance Criteria:**
  - API endpoints exist for CRUD operations on deals.
  - Only authorized users can modify deals.
  - Deal data is validated and persisted.
- **Status:** ✅ Completed — Endpoints, models, and schemas are implemented in `backend/app/routers/deals.py`, `models.py`, and `schemas/deals.py`.

#### Feature: Account Management API
- **User Story:**
  - As a user, I want to create, view, update, and list accounts (companies/customers), so that I can manage and organize my sales relationships.
- **Acceptance Criteria:**
  - API endpoints exist for CRUD operations on accounts.
  - Only authorized users can modify accounts.
  - Account data is validated and persisted.
- **Status:** ⚠️ Partially Complete — Account models and schemas exist, and accounts are used in deal endpoints, but there is no dedicated Account API router yet.

#### Feature: Stakeholder Management API
- **User Story:**
  - As a user, I want to add, view, update, and list stakeholders (contacts/people) within accounts, so that I can track key decision-makers and influencers for each deal.
- **Acceptance Criteria:**
  - API endpoints exist for CRUD operations on stakeholders.
  - Stakeholders are linked to accounts and can be associated with deals.
  - Only authorized users can modify stakeholders.
  - Stakeholder data is validated and persisted.
- **Status:** ⚠️ Partially Complete — Stakeholder models and schemas exist, and stakeholders are included in deal responses, but there is no dedicated Stakeholder API router yet.

#### Feature: Task Management API
- **User Story:**
  - As a user, I want to create, view, update, and list tasks related to deals, accounts, or stakeholders, so that I can track and manage my sales activities.
- **Acceptance Criteria:**
  - API endpoints exist for CRUD operations on tasks.
  - Tasks can be linked to deals, accounts, or stakeholders.
  - Only authorized users can modify tasks.
  - Task data is validated and persisted.
- **Status:** ⬜ Not Yet Started — No task models, schemas, or endpoints found in the current codebase.

#### Feature: Basic Frontend Dashboard
- **User Story:**
  - As a user, I want a dashboard to view and manage my deals, tasks, stakeholders and accounts, so that I can easily track my work.
- **Acceptance Criteria:**
  - Dashboard displays deals, accounts, tasks, and stakeholders with key metrics (total deals, active deals, recent activity).
  - Users can navigate to details, filter/search by status/name/date, and access quick-add functionality for new items.
  - Dashboard provides visual indicators for deal health/priority, real-time updates, and recent activity feed.
  - Mobile-responsive design loads within 3 seconds and handles large datasets efficiently.

---

### 3. Intelligence & Analytics

#### Feature: Deal Intelligence View
- **User Story:**
  - As a user, I want to see a summary of each deal's health, MEDDPICC analysis, and key metrics, so that I can quickly assess deal status and risks.
- **Acceptance Criteria:**
  - Intelligence view aggregates deal, health, MEDDPICC, and evidence data.
  - Data is accurate and updates in real time.
  - Users can access intelligence from the dashboard.

#### Feature: Basic Usage Tracking
- **User Story:**
  - As an admin, I want to track user and tenant activity, so that I can monitor usage and plan for future analytics.
- **Acceptance Criteria:**
  - User and tenant actions are logged.
  - Usage data is accessible for reporting.

---

### 4. UI/UX & Frontend

#### Feature: UI/UX Polish for Key Flows
- **User Story:**
  - As a user, I want the interface to be clean and intuitive, so that I can complete tasks efficiently and enjoyably.
- **Acceptance Criteria:**
  - Key user flows (onboarding, dashboard, deal management) are tested and refined.
  - UI is responsive and visually consistent.
  - User feedback is incorporated.

---

### 5. Testing & Quality

#### Feature: Testing & Quality Assurance
- **User Story:**
  - As a stakeholder, I want critical paths to be covered by tests, so that we reduce the risk of major bugs at launch.
- **Acceptance Criteria:**
  - Unit and integration tests cover all critical features.
  - CI pipeline runs tests automatically.
  - Major bugs are resolved before launch.

---

### 6. Documentation

#### Feature: Prepare Documentation
- **User Story:**
  - As a user, I want onboarding guides and API documentation, so that I can get started quickly and understand how to use the product.
- **Acceptance Criteria:**
  - User guides and onboarding materials are available.
  - API documentation covers all endpoints.
  - Documentation is accessible from the app.

---

### 7. Launch & Feedback

#### Feature: MVP Beta/Soft Launch
- **User Story:**
  - As a product owner, I want to release the MVP to a small group for feedback, so that we can validate and improve before public launch.
- **Acceptance Criteria:**
  - Beta users are invited and onboarded.
  - Feedback is collected and reviewed.
  - Critical issues are addressed before public launch.

#### Feature: Public MVP Launch
- **User Story:**
  - As a stakeholder, I want to launch the MVP to the public, so that we can begin broader adoption and gather real-world feedback.
- **Acceptance Criteria:**
  - MVP is released to the public or target audience.
  - Launch is communicated to stakeholders.
  - Post-launch monitoring and support are in place.

---

## Sign-Off

- [ ] All stakeholders have reviewed and approved this document. 