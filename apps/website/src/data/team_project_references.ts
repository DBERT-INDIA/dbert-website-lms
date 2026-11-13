// src/data/team_project_references.ts
// Production project references and verified pre-vetted engineers who contributed to them.
// Generated from master certificates registry with 100% cryptographic parity.

export interface ProjectContributor {
  name: string;
  certId: string;
  domain: string;
  score: number;
  grade: string;
  duration: string;
  verifyUrl: string;
}

export interface ProjectReference {
  id: string;
  title: string;
  badge: string;
  tagline: string;
  category: string;
  description: string;
  stack: string[];
  portfolioUrl?: string | null;
  totalContributors: number;
  contributors: ProjectContributor[];
}

export const TEAM_PROJECT_REFERENCES: ProjectReference[] = [
  {
    "id": "gayatri-ai",
    "title": "Gayatri AI",
    "badge": "Flagship Incubated Venture",
    "tagline": "Enterprise Educational Intelligence & RAG Knowledge Architecture",
    "category": "Applied AI & LLM Systems",
    "description": "Multi-agent cognitive educational platform featuring concept graphs, retrieval-augmented pedagogical guidance, and automated assessment pipelines.",
    "stack": [
      "Python",
      "PyTorch",
      "LangChain",
      "FastAPI",
      "Next.js",
      "PostgreSQL"
    ],
    "portfolioUrl": null,
    "totalContributors": 38,
    "contributors": [
      {
        "name": "Rukanana Mounika",
        "certId": "CERT-DBERT-2026-AIML-104",
        "domain": "Artificial Intelligence & Machine Learning",
        "score": 88,
        "grade": "Grade: A+ (Outstanding Performance)",
        "duration": "15 August 2026 \u2013 15 October 2026 (2 Months)",
        "verifyUrl": "/verify/CERT-DBERT-2026-AIML-104"
      },
      {
        "name": "Arijit Shaw",
        "certId": "CERT-DBERT-2026-PA-021",
        "domain": "Python Automation",
        "score": 87,
        "grade": "Grade: A+ (Outstanding Performance)",
        "duration": "August to October 2026 (2 Months)",
        "verifyUrl": "/verify/CERT-DBERT-2026-PA-021"
      },
      {
        "name": "Harshpreet Singh",
        "certId": "CERT-DBERT-2026-AIML-006",
        "domain": "Artificial Intelligence & Machine Learning",
        "score": 87,
        "grade": "Grade: A+ (Outstanding Performance)",
        "duration": "August to October 2026 (2 Months)",
        "verifyUrl": "/verify/CERT-DBERT-2026-AIML-006"
      },
      {
        "name": "Jay Kumar",
        "certId": "CERT-DBERT-2026-FSD-051",
        "domain": "Full Stack Development",
        "score": 87,
        "grade": "Grade: A+ (Outstanding Performance)",
        "duration": "August to October 2026 (2 Months)",
        "verifyUrl": "/verify/CERT-DBERT-2026-FSD-051"
      },
      {
        "name": "Kartik Suchak",
        "certId": "CERT-DBERT-2026-AIML-011",
        "domain": "Artificial Intelligence & Machine Learning",
        "score": 87,
        "grade": "Grade: A+ (Outstanding Performance)",
        "duration": "May to July 2026 (2 Months)",
        "verifyUrl": "/verify/CERT-DBERT-2026-AIML-011"
      },
      {
        "name": "Kshitiz Malviya",
        "certId": "CERT-DBERT-2026-AIML-036",
        "domain": "Artificial Intelligence & Machine Learning",
        "score": 87,
        "grade": "Grade: A+ (Outstanding Performance)",
        "duration": "August to October 2026 (2 Months)",
        "verifyUrl": "/verify/CERT-DBERT-2026-AIML-036"
      },
      {
        "name": "Naincy Srivastava",
        "certId": "CERT-DBERT-2026-DA-054",
        "domain": "Data Analyst",
        "score": 87,
        "grade": "Grade: A+ (Outstanding Performance)",
        "duration": "August to October 2026 (2 Months)",
        "verifyUrl": "/verify/CERT-DBERT-2026-DA-054"
      },
      {
        "name": "Potnuru Pravallika",
        "certId": "CERT-DBERT-2026-FSD-028",
        "domain": "Full Stack Development",
        "score": 87,
        "grade": "Grade: A+ (Outstanding Performance)",
        "duration": "August to October 2026 (2 Months)",
        "verifyUrl": "/verify/CERT-DBERT-2026-FSD-028"
      },
      {
        "name": "Priyanshi Choudhary",
        "certId": "CERT-DBERT-2026-AIML-029",
        "domain": "Artificial Intelligence & Machine Learning",
        "score": 87,
        "grade": "Grade: A+ (Outstanding Performance)",
        "duration": "August to October 2026 (2 Months)",
        "verifyUrl": "/verify/CERT-DBERT-2026-AIML-029"
      },
      {
        "name": "Rajkumar Ahirwar",
        "certId": "CERT-DBERT-2026-AIML-039",
        "domain": "Artificial Intelligence & Machine Learning",
        "score": 87,
        "grade": "Grade: A+ (Outstanding Performance)",
        "duration": "August to October 2026 (2 Months)",
        "verifyUrl": "/verify/CERT-DBERT-2026-AIML-039"
      },
      {
        "name": "Rapolu Abhishek",
        "certId": "CERT-DBERT-2026-AIML-014",
        "domain": "Artificial Intelligence & Machine Learning",
        "score": 87,
        "grade": "Grade: A+ (Outstanding Performance)",
        "duration": "July to September 2026 (2 Months)",
        "verifyUrl": "/verify/CERT-DBERT-2026-AIML-014"
      },
      {
        "name": "Sakthi P",
        "certId": "CERT-DBERT-2026-DA-022",
        "domain": "Data Analyst",
        "score": 87,
        "grade": "Grade: A+ (Outstanding Performance)",
        "duration": "August to October 2026 (2 Months)",
        "verifyUrl": "/verify/CERT-DBERT-2026-DA-022"
      },
      {
        "name": "Shanmuga Priya",
        "certId": "CERT-DBERT-2026-DA-047",
        "domain": "Data Analyst",
        "score": 87,
        "grade": "Grade: A+ (Outstanding Performance)",
        "duration": "August to October 2026 (2 Months)",
        "verifyUrl": "/verify/CERT-DBERT-2026-DA-047"
      },
      {
        "name": "Shanu Sri Gowtham",
        "certId": "CERT-DBERT-2026-AIML-013",
        "domain": "Artificial Intelligence & Machine Learning",
        "score": 87,
        "grade": "Grade: A+ (Outstanding Performance)",
        "duration": "August to October 2026 (2 Months)",
        "verifyUrl": "/verify/CERT-DBERT-2026-AIML-013"
      },
      {
        "name": "Subhradip Das",
        "certId": "CERT-DBERT-2026-FSD-043",
        "domain": "Full Stack Development",
        "score": 87,
        "grade": "Grade: A+ (Outstanding Performance)",
        "duration": "August to October 2026 (2 Months)",
        "verifyUrl": "/verify/CERT-DBERT-2026-FSD-043"
      },
      {
        "name": "Vansh Choudhary",
        "certId": "CERT-DBERT-2026-DA-012",
        "domain": "Data Analyst",
        "score": 87,
        "grade": "Grade: A+ (Outstanding Performance)",
        "duration": "August to October 2026 (2 Months)",
        "verifyUrl": "/verify/CERT-DBERT-2026-DA-012"
      },
      {
        "name": "Vansh Choudhary",
        "certId": "CERT-DBERT-2026-DA-015",
        "domain": "Data Analyst",
        "score": 87,
        "grade": "Grade: A+ (Outstanding Performance)",
        "duration": "August to October 2026 (2 Months)",
        "verifyUrl": "/verify/CERT-DBERT-2026-DA-015"
      },
      {
        "name": "Vishwajeet Shinde",
        "certId": "CERT-DBERT-2026-DA-027",
        "domain": "Data Analyst",
        "score": 87,
        "grade": "Grade: A+ (Outstanding Performance)",
        "duration": "August to October 2026 (2 Months)",
        "verifyUrl": "/verify/CERT-DBERT-2026-DA-027"
      },
      {
        "name": "Shreyash Sambhaji Kamble",
        "certId": "CERT-DBERT-2026-DA-077",
        "domain": "Data Analyst",
        "score": 86,
        "grade": "Grade: A+ (Outstanding Performance)",
        "duration": "May to July 2026 (2 Months)",
        "verifyUrl": "/verify/CERT-DBERT-2026-DA-077"
      },
      {
        "name": "Arnak Ray",
        "certId": "CERT-DBERT-2026-AIML-050",
        "domain": "Artificial Intelligence & Machine Learning",
        "score": 85,
        "grade": "Grade: A+ (Outstanding Performance)",
        "duration": "July to September 2026 (2 Months)",
        "verifyUrl": "/verify/CERT-DBERT-2026-AIML-050"
      },
      {
        "name": "Gurveer Singh",
        "certId": "CERT-DBERT-2026-UIUX-026",
        "domain": "UI & UX Design",
        "score": 85,
        "grade": "Grade: A+ (Outstanding Performance)",
        "duration": "August to October 2026 (2 Months)",
        "verifyUrl": "/verify/CERT-DBERT-2026-UIUX-026"
      },
      {
        "name": "Molli Mokshitha Ram",
        "certId": "CERT-DBERT-2026-AIML-079",
        "domain": "Artificial Intelligence & Machine Learning",
        "score": 85,
        "grade": "Grade: A+ (Outstanding Performance)",
        "duration": "15 August 2026 \u2013 15 October 2026 (2 Months)",
        "verifyUrl": "/verify/CERT-DBERT-2026-AIML-079"
      },
      {
        "name": "Nikita Khandu Ghuge",
        "certId": "CERT-DBERT-2026-AIML-034",
        "domain": "Artificial Intelligence & Machine Learning",
        "score": 85,
        "grade": "Grade: A+ (Outstanding Performance)",
        "duration": "August to October 2026 (2 Months)",
        "verifyUrl": "/verify/CERT-DBERT-2026-AIML-034"
      },
      {
        "name": "Shanmukha Sri Saikumar Medisetty",
        "certId": "CERT-DBERT-2026-AIML-002",
        "domain": "Artificial Intelligence & Machine Learning",
        "score": 85,
        "grade": "Grade: A+ (Outstanding Performance)",
        "duration": "August to October 2026 (2 Months)",
        "verifyUrl": "/verify/CERT-DBERT-2026-AIML-002"
      },
      {
        "name": "Kushal Agarwal",
        "certId": "CERT-DBERT-2026-DA-001",
        "domain": "Data Analyst",
        "score": 84,
        "grade": "Grade: A (Very Good Performance)",
        "duration": "July to September 2026 (2 Months)",
        "verifyUrl": "/verify/CERT-DBERT-2026-DA-001"
      },
      {
        "name": "Malavika S",
        "certId": "CERT-DBERT-2026-FSD-025",
        "domain": "Full Stack Development",
        "score": 84,
        "grade": "Grade: A (Very Good Performance)",
        "duration": "June to August 2026 (2 Months)",
        "verifyUrl": "/verify/CERT-DBERT-2026-FSD-025"
      },
      {
        "name": "Oishani Majumder",
        "certId": "CERT-DBERT-2026-DA-009",
        "domain": "Data Analyst",
        "score": 84,
        "grade": "Grade: A (Very Good Performance)",
        "duration": "August to October 2026 (2 Months)",
        "verifyUrl": "/verify/CERT-DBERT-2026-DA-009"
      },
      {
        "name": "Shivani Dnyaneshwar Bawaskar",
        "certId": "CERT-DBERT-2026-DA-033",
        "domain": "Data Analyst",
        "score": 84,
        "grade": "Grade: A (Very Good Performance)",
        "duration": "August to October 2026 (2 Months)",
        "verifyUrl": "/verify/CERT-DBERT-2026-DA-033"
      },
      {
        "name": "Vikram Jangir",
        "certId": "CERT-DBERT-2026-DA-041",
        "domain": "Data Analyst",
        "score": 84,
        "grade": "Grade: A (Very Good Performance)",
        "duration": "June to August 2026 (2 Months)",
        "verifyUrl": "/verify/CERT-DBERT-2026-DA-041"
      },
      {
        "name": "Pulluri Bhargavi",
        "certId": "CERT-DBERT-2026-DA-048",
        "domain": "Data Analyst",
        "score": 83,
        "grade": "Grade: A (Very Good Performance)",
        "duration": "August to October 2026 (2 Months)",
        "verifyUrl": "/verify/CERT-DBERT-2026-DA-048"
      },
      {
        "name": "Thukakula Gayathree",
        "certId": "CERT-DBERT-2026-DA-032",
        "domain": "Data Analyst",
        "score": 83,
        "grade": "Grade: A (Very Good Performance)",
        "duration": "August to October 2026 (2 Months)",
        "verifyUrl": "/verify/CERT-DBERT-2026-DA-032"
      },
      {
        "name": "Vinisha",
        "certId": "CERT-DBERT-2026-AIML-075",
        "domain": "Artificial Intelligence & Machine Learning",
        "score": 83,
        "grade": "Grade: A (Very Good Performance)",
        "duration": "15 August 2026 \u2013 15 October 2026 (2 Months)",
        "verifyUrl": "/verify/CERT-DBERT-2026-AIML-075"
      },
      {
        "name": "Yogesh",
        "certId": "CERT-DBERT-2026-FSD-008",
        "domain": "Full Stack Development",
        "score": 83,
        "grade": "Grade: A (Very Good Performance)",
        "duration": "August to October 2026 (2 Months)",
        "verifyUrl": "/verify/CERT-DBERT-2026-FSD-008"
      },
      {
        "name": "Vasu Rakholiya",
        "certId": "CERT-DBERT-2026-DA-183",
        "domain": "Data Analyst",
        "score": 82,
        "grade": "Grade: A (Very Good Performance)",
        "duration": "August to October 2026 (2 Months)",
        "verifyUrl": "/verify/CERT-DBERT-2026-DA-183"
      },
      {
        "name": "deepanshu",
        "certId": "CERT-DBERT-2026-DA-186",
        "domain": "Data Analyst",
        "score": 81,
        "grade": "Grade: A (Very Good Performance)",
        "duration": "August to October 2026 (2 Months)",
        "verifyUrl": "/verify/CERT-DBERT-2026-DA-186"
      },
      {
        "name": "GURKA VINAY KUMAR REDDY",
        "certId": "CERT-DBERT-2026-AIML-169",
        "domain": "Artificial Intelligence & Machine Learning",
        "score": 80,
        "grade": "Grade: A (Very Good Performance)",
        "duration": "15 July 2026 \u2013 15 September 2026 (2 Months)",
        "verifyUrl": "/verify/CERT-DBERT-2026-AIML-169"
      },
      {
        "name": "M Brahmani",
        "certId": "CERT-DBERT-2026-DA-117",
        "domain": "Data Analyst",
        "score": 79,
        "grade": "Grade: A (Very Good Performance)",
        "duration": "August to October 2026 (2 Months)",
        "verifyUrl": "/verify/CERT-DBERT-2026-DA-117"
      },
      {
        "name": "N Deekshitha",
        "certId": "CERT-DBERT-2026-AIML-092",
        "domain": "Artificial Intelligence & Machine Learning",
        "score": 78,
        "grade": "Grade: A (Very Good Performance)",
        "duration": "August to October 2026 (2 Months)",
        "verifyUrl": "/verify/CERT-DBERT-2026-AIML-092"
      }
    ]
  },
  {
    "id": "alkame",
    "title": "Alkame Markets",
    "badge": "Quantitative Research Venture",
    "tagline": "Quantitative Market Intelligence & Conformal Prediction Engine",
    "category": "FinTech & Distributed Systems",
    "description": "Financial time-series forecasting, uncertainty quantification with split conformal inference, and microsecond market event processing microservices.",
    "stack": [
      "Python",
      "Conformal Prediction",
      "QuantLib",
      "React",
      "AWS ECS",
      "Docker"
    ],
    "portfolioUrl": "/startups/portfolio/alkame",
    "totalContributors": 15,
    "contributors": [
      {
        "name": "Aman Garg",
        "certId": "CERT-DBERT-2026-FSD-117",
        "domain": "Full Stack Web Development",
        "score": 88,
        "grade": "Grade: A+ (Outstanding Performance)",
        "duration": "15 June 2026 \u2013 15 August 2026 (2 Months)",
        "verifyUrl": "/verify/CERT-DBERT-2026-FSD-117"
      },
      {
        "name": "Aditya Chauhan",
        "certId": "CERT-DBERT-2026-FSD-030",
        "domain": "Full Stack Development",
        "score": 87,
        "grade": "Grade: A+ (Outstanding Performance)",
        "duration": "August to October 2026 (2 Months)",
        "verifyUrl": "/verify/CERT-DBERT-2026-FSD-030"
      },
      {
        "name": "Ankur Sen",
        "certId": "CERT-DBERT-2026-DA-031",
        "domain": "Data Analyst",
        "score": 87,
        "grade": "Grade: A+ (Outstanding Performance)",
        "duration": "July to September 2026 (2 Months)",
        "verifyUrl": "/verify/CERT-DBERT-2026-DA-031"
      },
      {
        "name": "Bhargavi C K",
        "certId": "CERT-DBERT-2026-AIML-020",
        "domain": "Artificial Intelligence & Machine Learning",
        "score": 87,
        "grade": "Grade: A+ (Outstanding Performance)",
        "duration": "August to October 2026 (2 Months)",
        "verifyUrl": "/verify/CERT-DBERT-2026-AIML-020"
      },
      {
        "name": "Neha Choudhary",
        "certId": "CERT-DBERT-2026-DA-003",
        "domain": "Data Analyst",
        "score": 87,
        "grade": "Grade: A+ (Outstanding Performance)",
        "duration": "July to September 2026 (2 Months)",
        "verifyUrl": "/verify/CERT-DBERT-2026-DA-003"
      },
      {
        "name": "Radha Bhamodkar",
        "certId": "CERT-DBERT-2026-DA-019",
        "domain": "Data Analyst",
        "score": 87,
        "grade": "Grade: A+ (Outstanding Performance)",
        "duration": "August to October 2026 (2 Months)",
        "verifyUrl": "/verify/CERT-DBERT-2026-DA-019"
      },
      {
        "name": "Sipun Das",
        "certId": "CERT-DBERT-2026-FSD-007",
        "domain": "Full Stack Development",
        "score": 87,
        "grade": "Grade: A+ (Outstanding Performance)",
        "duration": "June to August 2026 (2 Months)",
        "verifyUrl": "/verify/CERT-DBERT-2026-FSD-007"
      },
      {
        "name": "Priyanshu Kalondia",
        "certId": "CERT-DBERT-2026-AIML-018",
        "domain": "Artificial Intelligence & Machine Learning",
        "score": 85,
        "grade": "Grade: A+ (Outstanding Performance)",
        "duration": "August to October 2026 (2 Months)",
        "verifyUrl": "/verify/CERT-DBERT-2026-AIML-018"
      },
      {
        "name": "Suraj Shivsunder Jha",
        "certId": "CERT-DBERT-2026-FSD-042",
        "domain": "Full Stack Development",
        "score": 85,
        "grade": "Grade: A+ (Outstanding Performance)",
        "duration": "May to July 2026 (2 Months)",
        "verifyUrl": "/verify/CERT-DBERT-2026-FSD-042"
      },
      {
        "name": "Aryan Bhakuni",
        "certId": "CERT-DBERT-2026-DA-017",
        "domain": "Data Analyst",
        "score": 84,
        "grade": "Grade: A (Very Good Performance)",
        "duration": "July to September 2026 (2 Months)",
        "verifyUrl": "/verify/CERT-DBERT-2026-DA-017"
      },
      {
        "name": "Priyanshu Kalondia",
        "certId": "CERT-DBERT-2026-AIML-016",
        "domain": "Artificial Intelligence & Machine Learning",
        "score": 83,
        "grade": "Grade: A (Very Good Performance)",
        "duration": "August to October 2026 (2 Months)",
        "verifyUrl": "/verify/CERT-DBERT-2026-AIML-016"
      },
      {
        "name": "Rajveer Singh",
        "certId": "CERT-DBERT-2026-AIML-100",
        "domain": "Artificial Intelligence & Machine Learning",
        "score": 83,
        "grade": "Grade: A (Very Good Performance)",
        "duration": "August to October 2026 (2 Months)",
        "verifyUrl": "/verify/CERT-DBERT-2026-AIML-100"
      },
      {
        "name": "Amit Yadav",
        "certId": "CERT-DBERT-2026-FSD-084",
        "domain": "Full Stack Web Development",
        "score": 82,
        "grade": "Grade: A (Very Good Performance)",
        "duration": "15 July 2026 \u2013 15 September 2026 (2 Months)",
        "verifyUrl": "/verify/CERT-DBERT-2026-FSD-084"
      },
      {
        "name": "Archita Bajpai",
        "certId": "CERT-DBERT-2026-FSD-062",
        "domain": "Full Stack Web Development",
        "score": 81,
        "grade": "Grade: A (Very Good Performance)",
        "duration": "15 July 2026 \u2013 15 September 2026 (2 Months)",
        "verifyUrl": "/verify/CERT-DBERT-2026-FSD-062"
      },
      {
        "name": "Satya Patil",
        "certId": "CERT-DBERT-2026-DA-109",
        "domain": "Data Analyst",
        "score": 79,
        "grade": "Grade: A (Very Good Performance)",
        "duration": "July to September 2026 (2 Months)",
        "verifyUrl": "/verify/CERT-DBERT-2026-DA-109"
      }
    ]
  },
  {
    "id": "dbert-cloud",
    "title": "DBERT Enterprise Cloud",
    "badge": "Core Infrastructure",
    "tagline": "Technical Incubation Architecture & Cryptographic Verification",
    "category": "Cloud Infrastructure & Platform Engineering",
    "description": "High-concurrency reverse proxy routing, cryptographic public credential registry, automated systemd orchestration, and Next.js standalone pipelines.",
    "stack": [
      "Next.js 16 App Router",
      "Node.js Standalone",
      "Nginx SSL",
      "PostgreSQL",
      "Systemd",
      "Linux EC2"
    ],
    "portfolioUrl": null,
    "totalContributors": 16,
    "contributors": [
      {
        "name": "Bhargavi Poola",
        "certId": "CERT-DBERT-2026-FSD-156",
        "domain": "Full Stack Web Development",
        "score": 88,
        "grade": "Grade: A+ (Outstanding Performance)",
        "duration": "9 Nov 2026 \u2013 9 Jan 2027 (2 Months)",
        "verifyUrl": "/verify/CERT-DBERT-2026-FSD-156"
      },
      {
        "name": "Ajay Mishra",
        "certId": "CERT-DBERT-2026-FSD-055",
        "domain": "Full Stack Development",
        "score": 87,
        "grade": "Grade: A+ (Outstanding Performance)",
        "duration": "August to October 2026 (2 Months)",
        "verifyUrl": "/verify/CERT-DBERT-2026-FSD-055"
      },
      {
        "name": "Anushka",
        "certId": "CERT-DBERT-2026-DA-004",
        "domain": "Data Analyst",
        "score": 87,
        "grade": "Grade: A+ (Outstanding Performance)",
        "duration": "August to October 2026 (2 Months)",
        "verifyUrl": "/verify/CERT-DBERT-2026-DA-004"
      },
      {
        "name": "Arman Sharma",
        "certId": "CERT-DBERT-2026-FSD-035",
        "domain": "Full Stack Development",
        "score": 87,
        "grade": "Grade: A+ (Outstanding Performance)",
        "duration": "August to October 2026 (2 Months)",
        "verifyUrl": "/verify/CERT-DBERT-2026-FSD-035"
      },
      {
        "name": "Burra Thanvesh",
        "certId": "CERT-DBERT-2026-AIML-023",
        "domain": "Artificial Intelligence & Machine Learning",
        "score": 87,
        "grade": "Grade: A+ (Outstanding Performance)",
        "duration": "May to July 2026 (2 Months)",
        "verifyUrl": "/verify/CERT-DBERT-2026-AIML-023"
      },
      {
        "name": "Mood Rajesh",
        "certId": "CERT-DBERT-2026-FSD-037",
        "domain": "Full Stack Development",
        "score": 87,
        "grade": "Grade: A+ (Outstanding Performance)",
        "duration": "August to October 2026 (2 Months)",
        "verifyUrl": "/verify/CERT-DBERT-2026-FSD-037"
      },
      {
        "name": "Upputhalla Kavya Sri",
        "certId": "CERT-DBERT-2026-AIML-038",
        "domain": "Artificial Intelligence & Machine Learning",
        "score": 87,
        "grade": "Grade: A+ (Outstanding Performance)",
        "duration": "June to August 2026 (2 Months)",
        "verifyUrl": "/verify/CERT-DBERT-2026-AIML-038"
      },
      {
        "name": "Yasharth Poddar",
        "certId": "CERT-DBERT-2026-FSD-046",
        "domain": "Full Stack Development",
        "score": 87,
        "grade": "Grade: A+ (Outstanding Performance)",
        "duration": "July to September 2026 (2 Months)",
        "verifyUrl": "/verify/CERT-DBERT-2026-FSD-046"
      },
      {
        "name": "Gupta Ankit Ramvijay",
        "certId": "CERT-DBERT-2026-DA-010",
        "domain": "Data Analyst",
        "score": 85,
        "grade": "Grade: A+ (Outstanding Performance)",
        "duration": "August to October 2026 (2 Months)",
        "verifyUrl": "/verify/CERT-DBERT-2026-DA-010"
      },
      {
        "name": "Janhvi singh",
        "certId": "CERT-DBERT-2026-DA-184",
        "domain": "Data Analyst",
        "score": 85,
        "grade": "Grade: A+ (Outstanding Performance)",
        "duration": "August to October 2026 (2 Months)",
        "verifyUrl": "/verify/CERT-DBERT-2026-DA-184"
      },
      {
        "name": "Kolloju Meghana",
        "certId": "CERT-DBERT-2026-DA-049",
        "domain": "Data Analyst",
        "score": 84,
        "grade": "Grade: A (Very Good Performance)",
        "duration": "August to October 2026 (2 Months)",
        "verifyUrl": "/verify/CERT-DBERT-2026-DA-049"
      },
      {
        "name": "Ankit Saini",
        "certId": "CERT-DBERT-2026-FSD-070",
        "domain": "Full Stack Development",
        "score": 83,
        "grade": "Grade: A (Very Good Performance)",
        "duration": "August to October 2026 (2 Months)",
        "verifyUrl": "/verify/CERT-DBERT-2026-FSD-070"
      },
      {
        "name": "Kundan Kumhar",
        "certId": "CERT-DBERT-2026-FSD-056",
        "domain": "Full Stack Development",
        "score": 83,
        "grade": "Grade: A (Very Good Performance)",
        "duration": "August to October 2026 (2 Months)",
        "verifyUrl": "/verify/CERT-DBERT-2026-FSD-056"
      },
      {
        "name": "Piyush",
        "certId": "CERT-DBERT-2026-DA-040",
        "domain": "Data Analyst",
        "score": 83,
        "grade": "Grade: A (Very Good Performance)",
        "duration": "June to August 2026 (2 Months)",
        "verifyUrl": "/verify/CERT-DBERT-2026-DA-040"
      },
      {
        "name": "Komma Hari Kesava",
        "certId": "CERT-DBERT-2026-DA-127",
        "domain": "Data Analyst",
        "score": 80,
        "grade": "Grade: A (Very Good Performance)",
        "duration": "July to September 2026 (2 Months)",
        "verifyUrl": "/verify/CERT-DBERT-2026-DA-127"
      },
      {
        "name": "Lucky kumar",
        "certId": "CERT-DBERT-2026-PA-023",
        "domain": "Python Automation",
        "score": 80,
        "grade": "Grade: A (Very Good Performance)",
        "duration": "August to October 2026 (2 Months)",
        "verifyUrl": "/verify/CERT-DBERT-2026-PA-023"
      }
    ]
  },
  {
    "id": "aivara",
    "title": "Aivara Autonomous Suite",
    "badge": "Agentic Operations",
    "tagline": "Autonomous AI Operations & Headless Agentic Workflows",
    "category": "Autonomous Agents & Workflow Automation",
    "description": "Headless browser automation daemons, WhatsApp CRM multi-account orchestration, and asynchronous task delivery engines with circuit breaker resiliency.",
    "stack": [
      "Python",
      "Playwright",
      "SQLite WAL",
      "FastAPI",
      "Distributed Task Queues"
    ],
    "portfolioUrl": null,
    "totalContributors": 6,
    "contributors": [
      {
        "name": "Danisaram Anji",
        "certId": "CERT-DBERT-2026-DA-005",
        "domain": "Data Analyst",
        "score": 87,
        "grade": "Grade: A+ (Outstanding Performance)",
        "duration": "August to October 2026 (2 Months)",
        "verifyUrl": "/verify/CERT-DBERT-2026-DA-005"
      },
      {
        "name": "Harsh Kumar",
        "certId": "CERT-DBERT-2026-FSD-052",
        "domain": "Full Stack Development",
        "score": 87,
        "grade": "Grade: A+ (Outstanding Performance)",
        "duration": "August to October 2026 (2 Months)",
        "verifyUrl": "/verify/CERT-DBERT-2026-FSD-052"
      },
      {
        "name": "Nishant Makwane",
        "certId": "CERT-DBERT-2026-DA-044",
        "domain": "Data Analyst",
        "score": 87,
        "grade": "Grade: A+ (Outstanding Performance)",
        "duration": "August to October 2026 (2 Months)",
        "verifyUrl": "/verify/CERT-DBERT-2026-DA-044"
      },
      {
        "name": "Shruthi Yuvnuv. V",
        "certId": "CERT-DBERT-2026-FSD-045",
        "domain": "Full Stack Development",
        "score": 87,
        "grade": "Grade: A+ (Outstanding Performance)",
        "duration": "August to October 2026 (2 Months)",
        "verifyUrl": "/verify/CERT-DBERT-2026-FSD-045"
      },
      {
        "name": "Smit Ritesh Shah",
        "certId": "CERT-DBERT-2026-DA-053",
        "domain": "Data Analyst",
        "score": 87,
        "grade": "Grade: A+ (Outstanding Performance)",
        "duration": "August to October 2026 (2 Months)",
        "verifyUrl": "/verify/CERT-DBERT-2026-DA-053"
      },
      {
        "name": "Rohit Ranjan Tiwari",
        "certId": "CERT-DBERT-2026-DA-124",
        "domain": "Data Analyst",
        "score": 81,
        "grade": "Grade: A (Very Good Performance)",
        "duration": "August to October 2026 (2 Months)",
        "verifyUrl": "/verify/CERT-DBERT-2026-DA-124"
      }
    ]
  },
  {
    "id": "cognitive-solutions",
    "title": "Cognitive Solutions",
    "badge": "Enterprise Analytics",
    "tagline": "Business Intelligence & Dimensional Data Warehousing Suite",
    "category": "Enterprise Data Analytics",
    "description": "End-to-end data pipelines, executive KPI dash-cards, dimensional Star schema modeling, and automated data quality audits for enterprise telemetry.",
    "stack": [
      "SQL",
      "Data Warehousing",
      "Tableau",
      "PowerBI",
      "Python ETL",
      "Statistical Modeling"
    ],
    "portfolioUrl": null,
    "totalContributors": 5,
    "contributors": [
      {
        "name": "Sakthi P",
        "certId": "CERT-DBERT-2026-DA-185",
        "domain": "Data Analyst",
        "score": 86,
        "grade": "Grade: A+ (Outstanding Performance)",
        "duration": "15 August 2026 \u2013 15 October 2026 (2 Months)",
        "verifyUrl": "/verify/CERT-DBERT-2026-DA-185"
      },
      {
        "name": "Siva Sankar Thirumalasetty",
        "certId": "CERT-DBERT-2026-DA-067",
        "domain": "Data Analyst",
        "score": 84,
        "grade": "Grade: A (Very Good Performance)",
        "duration": "15 August 2026 \u2013 15 October 2026 (2 Months)",
        "verifyUrl": "/verify/CERT-DBERT-2026-DA-067"
      },
      {
        "name": "Bharathan K",
        "certId": "CERT-DBERT-2026-DA-112",
        "domain": "Data Analyst",
        "score": 82,
        "grade": "Grade: A (Very Good Performance)",
        "duration": "15 August 2026 \u2013 15 October 2026 (2 Months)",
        "verifyUrl": "/verify/CERT-DBERT-2026-DA-112"
      },
      {
        "name": "OM VINAYAK TRIPATHY",
        "certId": "CERT-DBERT-2026-DA-083",
        "domain": "Data Analyst",
        "score": 81,
        "grade": "Grade: A (Very Good Performance)",
        "duration": "15 August 2026 \u2013 15 October 2026 (2 Months)",
        "verifyUrl": "/verify/CERT-DBERT-2026-DA-083"
      },
      {
        "name": "CHINTHALA SATHISH KUMAR",
        "certId": "CERT-DBERT-2026-DA-113",
        "domain": "Data Analyst",
        "score": 80,
        "grade": "Grade: A (Very Good Performance)",
        "duration": "15 August 2026 \u2013 15 October 2026 (2 Months)",
        "verifyUrl": "/verify/CERT-DBERT-2026-DA-113"
      }
    ]
  },
  {
    "id": "dbert-design-system",
    "title": "DBERT Sovereign Interface",
    "badge": "Design Engineering",
    "tagline": "Cyber-Industrial Design System & Design Tokens",
    "category": "UI/UX & Design Engineering",
    "description": "Foundry aesthetic typography, high-density dashboard layouts, WCAG AAA accessibility contrast tokens, and SVG micro-interactions.",
    "stack": [
      "Figma Tokens",
      "CSS Variables",
      "Next.js",
      "Design Tokens",
      "Responsive Grid"
    ],
    "portfolioUrl": null,
    "totalContributors": 1,
    "contributors": [
      {
        "name": "Devanshi Yadac",
        "certId": "CERT-DBERT-2026-UIUX-041",
        "domain": "UI/UX Prototyping & Design",
        "score": 87,
        "grade": "Grade: A+ (Outstanding Performance)",
        "duration": "15 May 2026 \u2013 15 July 2026 (2 Months)",
        "verifyUrl": "/verify/CERT-DBERT-2026-UIUX-041"
      }
    ]
  }
];
