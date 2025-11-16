# 🤖 Smart Subsidy Complaints AI Platform

<table style="border-collapse: collapse; border-spacing: 0;">
  <tr style="border: none;">
    <td align="left" width="140" style="border:none;">
      <img src="./Images/Others/DataFlow.jpg" width="140" style="border-radius: 50%;border: 3px solid #718096" alt="Team Logo"/>
    </td>
    <td align="left" valign="middle" style="border:none;">
      <h1 style="margin: 0; font-size: 40px;">DataFlow</h1>
        <p>
        <img src="https://img.shields.io/badge/Status-In%20Progress-blue" alt="Project Status"/>
        <img src="https://img.shields.io/badge/Apache%20Kafka-2.8.1-000000?logo=apachekafka" alt="Kafka"/>
        <img src="https://img.shields.io/badge/Apache%20Spark-3.2.0-E25A1C?logo=apachespark" alt="Spark"/>
        <img src="https://custom-icon-badges.demolab.com/badge/-2.3.3-017CEE?logo=airflow-ge&style=flat&label=Apache Airflow" alt="Airflow"/>
        <img src="https://img.shields.io/badge/Streamlit-1.10.0-FF4B4B?logo=streamlit" alt="Streamlit"/>
        <img src="https://img.shields.io/badge/Hugging%20Face-Transformers-FFD21E.svg?logo=huggingface" alt="Hugging Face"/>
        <img src="https://img.shields.io/badge/Docker-20.10-2496ED?logo=docker" alt="Docker"/>
        </p>
    </td>
  </tr>
</table>

---

## 📖 About The Project

This project aims to build an **AI-powered Big Data platform** for managing and analyzing subsidy-related complaints in Arabic. It enables **real-time collection, processing, and analysis** of citizen complaints to improve **transparency, efficiency, and service quality**.

The system combines **Streamlit, Kafka, Spark, Airflow, and PostgreSQL** inside a fully containerized **Docker** environment to automate the data flow from initial submission to final insight.

This project was created for the **AI & Data Science Track - Round 3** of the **Digital Egypt Pioneers** program, sponsored by the **Ministry of Communications and Information Technology**.

### ✨ Core Features

- **Real-Time Ingestion:** A Streamlit web app captures user complaints and sends them instantly to a Kafka topic.
- **AI-Powered Classification:** A fine-tuned **`arabert`** model from Hugging Face performs multi-label classification to categorize complaints (e.g., `BREAD_QUALITY`, `STAFF_BEHAVIOR`, `CARD_ISSUE`).
- **Scalable Stream Processing:** **Apache Spark** (Structured Streaming) consumes data from Kafka, applies AI model inference in real-time, and writes structured results to PostgreSQL.
- **Workflow Orchestration:** **Apache Airflow** manages scheduled batch jobs, such as generating daily summary reports.
- **Interactive Dashboard:** A second Streamlit page queries the PostgreSQL database to display real-time analytics, charts, and key performance indicators.

---

## 🏗️ Architecture Overview

![Architecture Diagram](./Images/Others/project_architecture.png)

---

## 🛠️ Technologies & Tools

| Category              | Technology                  | Purpose                                                                        |
| :-------------------- | :-------------------------- | :----------------------------------------------------------------------------- |
| **Containerization**  | Docker & Docker Compose     | To build, run, and manage all services in an isolated environment.             |
| **User Interface**    | Streamlit                   | For the complaint submission form and the analytics dashboard.                 |
| **Message Broker**    | Apache Kafka & Zookeeper    | For real-time, fault-tolerant data ingestion as a message queue.               |
| **Stream Processing** | Apache Spark                | To consume from Kafka, run AI model inference, and process data.               |
| **AI & NLP**          | Hugging Face `transformers` | To load and fine-tune the `arabert` model for multi-label text classification. |
| **Orchestration**     | Apache Airflow              | To schedule and monitor batch data pipelines (e.g., daily reports).            |
| **Database**          | PostgreSQL                  | To store the structured, analyzed complaint data for the dashboard.            |
| **Monitoring**        | Kafka UI                    | To easily view topics and messages in the Kafka cluster.                       |

---

## 📊 Project Milestones

This project is being built in the following phases:

- **Milestone 1: Foundations & Data Preparation**

  - Define the multi-label classification schema and create a labeled dataset of 500-1,000 Arabic complaints.

- **Milestone 2: The End-to-End "Skeleton" Pipeline**

  - Build the full data pipeline (`Streamlit` -> `Kafka` -> `Spark` -> `PostgreSQL`) using a **"dummy" AI model** to ensure the plumbing works.

- **Milestone 3: The AI Model (Fine-Tuning)**

  - Use the labeled data from Milestone 1 to fine-tune the `arabert` model for our specific complaint categories.

- **Milestone 4: Integration, Orchestration & Polish**

  - Replace the "dummy" logic in the Spark job with the real, fine-tuned AI model using a Pandas UDF.
  - Build an Airflow DAG for a daily summary report.

- **Milestone 5: Final Testing & Documentation**
  - Perform end-to-end testing and finalize all project documentation.

---

## 👥 Team Members

<div style="display: flex; justify-content: center;">
  <div align="center" style="background: linear-gradient(135deg, #2d3748 0%, #4a5568 100%); padding: 30px; border-radius: 15px; box-shadow: 0 4px 6px   rgba(0,0,0,0.3);">
    <p><b style="font-size: 20px; color: #e2e8f0;">Meet Our Team</b><p>
    <table style="border-collapse: collapse; border-spacing: 0;">
      <tr style="border: none;">
        <td align="center" width="180px" style="border: none; padding: 15px;">
          <img src="./Images/Team/medhat_mohamed.jpg" width="150px" style="border-radius: 50%; border: 3px solid #e2e8f0; box-shadow: 0 0 8px rgba(255,  255,255,0.1);" alt="Medhat Mohamed Ezzat"/><br/>
          <sub><b style="font-size: 15px; color: #e2e8f0;">Medhat Mohamed Ezzat</b></sub><br/>
          <div style="margin-top: 8px;">
            <a href="https://www.linkedin.com/in/medhat-mohamed-ezzat-03a58b235">
              <img src="https://img.icons8.com/color/24/000000/linkedin.png" alt="LinkedIn"/>
            </a>
            <a href="https://www.github.com/medhat2525548">
              <img src="https://img.icons8.com/ios-glyphs/24/ffffff/github.png" alt="GitHub"/>
            </a>
            <a href="mailto:medhatsaid56@gmail.com">
              <img src="https://img.icons8.com/?size=24&id=P7UIlhbpWzZm" alt="Email"/>
            </a>
          </div>
        </td>
        <td align="center" width="180px" style="border: none; padding: 15px;">
          <img src="./Images/Team/rawan_nada.jpg" width="150px" style="border-radius: 50%; border: 3px solid #e2e8f0; box-shadow: 0 0 8px rgba(255,255,  255,0.1);" alt="Rawan Samy Nada"/><br/>
          <sub><b style="font-size: 15px; color: #e2e8f0;">Rawan Samy Nada</b></sub><br/>
          <div style="margin-top: 8px;">
            <a href="https://www.linkedin.com/in/rawan-nada-a63994281">
              <img src="https://img.icons8.com/color/24/000000/linkedin.png" alt="LinkedIn"/>
            </a>
            <a href="https://www.github.com/Rawannada">
              <img src="https://img.icons8.com/ios-glyphs/24/ffffff/github.png" alt="GitHub"/>
            </a>
            <a href="mailto:Rwannada22@gmail.com">
              <img src="https://img.icons8.com/?size=24&id=P7UIlhbpWzZm" alt="Email"/>
            </a>
          </div>
        </td>
        <td align="center" width="180px" style="border: none; padding: 15px;">
          <img src="./Images/Team/george_ezzat.jpg" width="150px" style="border-radius: 50%; border: 3px solid #e2e8f0; box-shadow: 0 0 8px rgba(255,  255,255,0.1);" alt="George Ezzat Hosni"/><br/>
          <sub><b style="font-size: 15px; color: #e2e8f0;">George Ezzat Hosni</b></sub><br/>
          <div style="margin-top: 8px;">
            <a href="https://www.linkedin.com/in/george-ezat">
              <img src="https://img.icons8.com/color/24/000000/linkedin.png" alt="LinkedIn"/>
            </a>
            <a href="https://www.github.com/george-ezat">
              <img src="https://img.icons8.com/ios-glyphs/24/ffffff/github.png" alt="GitHub"/>
            </a>
            <a href="mailto:e.georgeezat@gmail.com">
              <img src="https://img.icons8.com/?size=24&id=P7UIlhbpWzZm" alt="Email"/>
            </a>
          </div>
        </td>
      </tr>
      <tr style="border: none;">
        <td align="center" width="180px" style="border: none; padding: 15px;">
          <img src="./Images/Team/farah_maurice.jpg" width="150px" style="border-radius: 50%; border: 3px solid #e2e8f0; box-shadow: 0 0 8px rgba(255,  255,255,0.1);" alt="Farah Maurice Wanis"/><br/>
          <sub><b style="font-size: 15px; color: #e2e8f0;">Farah Maurice Wanis</b></sub><br/>
          <div style="margin-top: 8px;">
            <a href="https://www.linkedin.com/in/farah-maurice-058b20259">
              <img src="https://img.icons8.com/color/24/000000/linkedin.png" alt="LinkedIn"/>
            </a>
            <a href="https://www.github.com/Farahmaurice">
              <img src="https://img.icons8.com/ios-glyphs/24/ffffff/github.png" alt="GitHub"/>
            </a>
            <a href="mailto:farahmaurice3@gmail.com">
              <img src="https://img.icons8.com/?size=24&id=P7UIlhbpWzZm" alt="Email"/>
            </a>
          </div>
        </td>
        <td align="center" width="180px" style="border: none; padding: 15px;">
          <img src="./Images/Team/david_sameh.jpg" width="150px" style="border-radius: 50%; border: 3px solid #e2e8f0; box-shadow: 0 0 8px rgba(255,  255,255,0.1);" alt="David Sameh Fouad"/><br/>
          <sub><b style="font-size: 15px; color: #e2e8f0;">David Sameh Fouad</b></sub><br/>
          <div style="margin-top: 8px;">
            <a href="https://www.linkedin.com/in/davidsamehfouad">
              <img src="https://img.icons8.com/color/24/000000/linkedin.png" alt="LinkedIn"/>
            </a>
            <a href="https://www.github.com/DavidSFouad">
              <img src="https://img.icons8.com/ios-glyphs/24/ffffff/github.png" alt="GitHub"/>
            </a>
            <a href="mailto:davidsameh302@gmail.com">
              <img src="https://img.icons8.com/?size=24&id=P7UIlhbpWzZm" alt="Email"/>
            </a>
          </div>
        </td>
        <td align="center" width="180px" style="border: none; padding: 15px;">
          <img src="./Images/Team/jana_amr.jpg" width="150px" style="border-radius: 50%; border: 3px solid #e2e8f0; box-shadow: 0 0 8px rgba(255,255,  255,0.1);" alt="Jana Amr Adbul Hamid"/><br/>
          <sub><b style="font-size: 15px; color: #e2e8f0;">Jana Amr Abdelhamed</b></sub><br/>
          <div style="margin-top: 8px;">
            <a href="https://www.linkedin.com/in/jana-amr-0362852b0">
              <img src="https://img.icons8.com/color/24/000000/linkedin.png" alt="LinkedIn"/>
            </a>
            <a href="https://www.github.com/Jaanaamrr">
              <img src="https://img.icons8.com/ios-glyphs/24/ffffff/github.png" alt="GitHub"/>
            </a>
            <a href="mailto:j.amr2313@nu.edu.eg">
              <img src="https://img.icons8.com/?size=24&id=P7UIlhbpWzZm" alt="Email"/>
            </a>
          </div>
        </td>
      </tr>
    </table>
  </div>
</div>

---
