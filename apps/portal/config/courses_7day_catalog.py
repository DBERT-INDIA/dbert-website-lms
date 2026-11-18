"""
DBERT LMS - 7-Day Course Catalog for All Platform Domains
================================================================================
Defines complete, production-grade 7-day curricula (Days 1–7) for all 9 official
domains supported on DBERT platform, with 3 subtopics per chapter and daily quizzes.
================================================================================
"""

UI_UX_DESIGN_COURSE = {
    "domain": "UI/UX Design",
    "title": "UI/UX Design Systems, Figma Prototyping & Design Tokens",
    "slug": "ui-ux-design",
    "level": "Beginner",
    "estimated_hours": 14,
    "banner_gradient": "linear-gradient(135deg, #4c1d95 0%, #6d28d9 50%, #7c3aed 100%)",
    "chapters": [
        {
            "day_number": 1,
            "title": "Design Principles & User Experience Architecture",
            "subtopics": [
                (
                    "User Research, Personas & Information Architecture",
                    "Conduct qualitative user research, formulate persona archetypes, and construct logical sitemaps.",
                    [
                        "Qualitative user interviews, empathy mapping & problem framing",
                        "Information architecture, hierarchical taxonomy & card sorting",
                        "User journey mapping & touchpoint identification"
                    ]
                ),
                (
                    "Wireframing & Low-Fidelity Prototyping",
                    "Translate raw user needs into structural grayscale layouts and iterative low-fidelity wireframes.",
                    [
                        "Visual hierarchy, Gutenberg diagram & F-pattern layouts",
                        "Rapid low-fidelity wireframing in Figma with standard UI kits",
                        "Validating user navigation flows before high-fidelity visual styling"
                    ]
                ),
                (
                    "Mental Models & User Journey Flowcharts",
                    "Align digital interface behaviors with intuitive human cognitive expectations and mental models.",
                    [
                        "Cognitive load reduction & Hick's Law application",
                        "Edge cases, branching user decisions & zero-state views",
                        "Documenting interactive states in FigJam and Figma flow diagrams"
                    ]
                )
            ],
            "quiz": [
                {
                    "id": 1,
                    "question": "What is the primary purpose of low-fidelity wireframing?",
                    "options": [
                        "Focus on structural layout and navigation flows without visual styling distractions",
                        "Select the final production color palette and font weights",
                        "Generate CSS styles and frontend React code automatically",
                        "Benchmark server database query response times"
                    ],
                    "correct_index": 0
                },
                {
                    "id": 2,
                    "question": "Why is user research conducted before visual interface design begins?",
                    "options": [
                        "To validate actual user pain points and avoid building features nobody needs",
                        "To fulfill formal project management compliance requirements only",
                        "To decrease client-side browser font rendering latency",
                        "To choose between cloud hosting server infrastructure providers"
                    ],
                    "correct_index": 0
                }
            ]
        },
        {
            "day_number": 2,
            "title": "Layout Grids, Typography & Visual Hierarchy",
            "subtopics": [
                (
                    "The 8pt Grid System & Spatial Layout Rules",
                    "Master spatial consistency using 8-point baseline grids across desktop, tablet, and mobile displays.",
                    [
                        "Mathematical rhythm with 4pt and 8pt spacing tokens",
                        "Column, gutter, and margin configurations for responsive breakpoints",
                        "Consistent spatial padding in cards, modals, and container shells"
                    ]
                ),
                (
                    "Modular Typography Scales & Optical Alignment",
                    "Establish cohesive type systems using mathematical modular scales and optimal line lengths.",
                    [
                        "Major third and perfect fourth typographic ratios",
                        "Optimal readability: line-height (140-160%) and character measure (45-75 chars)",
                        "Optical kerning, letter spacing tokens, and typographic hierarchy"
                    ]
                ),
                (
                    "Visual Hierarchy & WCAG Contrast Compliance",
                    "Direct user attention with deliberate scale, color contrast, and accessibility compliance standards.",
                    [
                        "WCAG 2.1 AA and AAA contrast compliance ratios (4.5:1 text, 3:1 UI)",
                        "Primary, secondary, and tertiary visual focal points",
                        "Accessible design for color-deficient vision (Protanopia/Deuteranopia)"
                    ]
                )
            ],
            "quiz": [
                {
                    "id": 1,
                    "question": "What is the minimum contrast ratio required by WCAG 2.1 AA for normal body text?",
                    "options": [
                        "4.5:1",
                        "2.0:1",
                        "7.0:1",
                        "1.5:1"
                    ],
                    "correct_index": 0
                },
                {
                    "id": 2,
                    "question": "Why is the 8pt grid system widely adopted in modern UI engineering?",
                    "options": [
                        "It scales cleanly across fractional pixel screen densities (1x, 2x, 3x) without subpixel blurring",
                        "It restricts the designer to only 8 distinct colors across the entire design system",
                        "It forces all fonts to be exactly 8 pixels in size",
                        "It is the only grid format supported by web browsers"
                    ],
                    "correct_index": 0
                }
            ]
        },
        {
            "day_number": 3,
            "title": "Figma Mastery: Auto-Layout, Components & Variant Matrices",
            "subtopics": [
                (
                    "Advanced Auto-Layout & Directional Flex Rules",
                    "Build fluid, responsive UI components that mirror CSS Flexbox behaviors inside Figma.",
                    [
                        "Vertical and horizontal auto-layout hierarchies with nested containers",
                        "Hug contents, Fixed dimensions, and Fill container sizing behaviors",
                        "Min/max width and height constraints for realistic cross-device testing"
                    ]
                ),
                (
                    "Component Variants & Dynamic Property Sets",
                    "Construct robust atomic design components utilizing variant matrices and Boolean properties.",
                    [
                        "Master components, component instances, and override rules",
                        "Variant property sets (size, state, role, icon placement)",
                        "Boolean toggles, text properties, and instance swappers"
                    ]
                ),
                (
                    "Interactive Component States & Micro-Triggers",
                    "Prototype realistic interactions within components using nested component states.",
                    [
                        "Default, Hover, Pressed, Focused, and Disabled button states",
                        "Checkbox and toggle switch interactive component transitions",
                        "Input field validation states (empty, active, error, success)"
                    ]
                )
            ],
            "quiz": [
                {
                    "id": 1,
                    "question": "In Figma Auto-Layout, which sizing option makes a child element stretch to fill the available container width?",
                    "options": [
                        "Fill container",
                        "Hug contents",
                        "Fixed width",
                        "Absolute position"
                    ],
                    "correct_index": 0
                },
                {
                    "id": 2,
                    "question": "What advantage do Component Properties (Booleans, Text, Instance Swap) provide over creating combinatorial variants?",
                    "options": [
                        "They drastically reduce file size and simplify component maintenance by eliminating redundant variant layers",
                        "They export the component directly as an iOS Swift file",
                        "They automatically optimize background images for high-DPI displays",
                        "They force the client browser to pre-render the page"
                    ],
                    "correct_index": 0
                }
            ]
        },
        {
            "day_number": 4,
            "title": "Design Tokens, Typography Scales & WCAG Accessibility",
            "subtopics": [
                (
                    "Design Token Architecture & Taxonomy",
                    "Structure design tokens into global, semantic, and component-specific abstraction layers.",
                    [
                        "Global primitive tokens (e.g. blue-500, spacing-16)",
                        "Semantic contextual tokens (e.g. surface-primary, text-danger)",
                        "Component-specific tokens (e.g. button-primary-bg-hover)"
                    ]
                ),
                (
                    "Color Palettes, Semantic Roles & Dark Mode Mapping",
                    "Engineer adaptable multi-theme color palettes supporting seamless light and dark mode switching.",
                    [
                        "Perceptually uniform color spaces (OKLCH / HSL) for consistent theme shades",
                        "Surface elevation, border containment, and text contrast tiers",
                        "Figma Variable Modes for 1-click theme switching (Light / Dark / High-Contrast)"
                    ]
                ),
                (
                    "Accessible Touch Targets & Focus States",
                    "Design accessible interactive controls adhering to mobile touch targets and keyboard accessibility.",
                    [
                        "Minimum 44x44px touch targets on mobile viewports",
                        "High-visibility keyboard focus rings (:focus-visible styling)",
                        "Screen reader accessibility considerations and aria labeling specs"
                    ]
                )
            ],
            "quiz": [
                {
                    "id": 1,
                    "question": "In design token architecture, what is the key benefit of semantic tokens (e.g. 'color-text-danger') over raw primitives (e.g. 'color-red-600')?",
                    "options": [
                        "Semantic tokens decouple interface role from raw values, allowing global themes like dark mode without modifying UI components",
                        "Semantic tokens are faster to process by the GPU than primitive colors",
                        "Semantic tokens automatically translate English UI text into 50 languages",
                        "Semantic tokens eliminate the need for QA testing"
                    ],
                    "correct_index": 0
                },
                {
                    "id": 2,
                    "question": "What is the recommended minimum touch target size for mobile UI elements according to accessibility guidelines?",
                    "options": [
                        "44 x 44 pixels",
                        "16 x 16 pixels",
                        "100 x 100 pixels",
                        "24 x 24 pixels"
                    ],
                    "correct_index": 0
                }
            ]
        },
        {
            "day_number": 5,
            "title": "High-Fidelity Micro-Interactions, Smart Animate & Interactive States",
            "subtopics": [
                (
                    "Smart Animate & Physics-Based Motion Easing",
                    "Produce cinematic high-fidelity screen transitions using matching layer names and custom Bezier curves.",
                    [
                        "Layer naming matching conventions for seamless Smart Animate tweening",
                        "Cubic Bezier curve timing: Ease-out for entrances, Ease-in for exits",
                        "Duration tuning: 150-300ms for micro-interactions, 300-500ms for page transitions"
                    ]
                ),
                (
                    "Complex Component Interactions & Scroll Overflows",
                    "Simulate production-grade user experiences with nested scroll zones and sticky headers.",
                    [
                        "Horizontal carousels with snap-to-card paging",
                        "Sticky navigation headers, bottom sheets, and floating action buttons (FAB)",
                        "Interactive multi-state forms with dynamic inline validation"
                    ]
                ),
                (
                    "Micro-Interactions, Hover Feedback & Haptics",
                    "Elevate delight and usability through subtle visual cues, skeleton loaders, and tactile feedback.",
                    [
                        "Subtle hover scale and elevation box-shadow transitions",
                        "Pulsing skeleton loader placeholders for asynchronous content",
                        "Success celebrations, checkmark animations, and error shake states"
                    ]
                )
            ],
            "quiz": [
                {
                    "id": 1,
                    "question": "When configuring Smart Animate between two frames in Figma, what must be identical for layers to transition smoothly instead of fading?",
                    "options": [
                        "Layer names and hierarchy location within the parent frame",
                        "The exact RGB hex color code of both parent frames",
                        "The creation timestamp of the two frames",
                        "The resolution of the designer's display monitor"
                    ],
                    "correct_index": 0
                },
                {
                    "id": 2,
                    "question": "What is the standard recommended duration range for UI micro-interactions (e.g. dropdown toggle, button press)?",
                    "options": [
                        "150ms to 300ms",
                        "1000ms to 2000ms",
                        "10ms to 20ms",
                        "5000ms to 7000ms"
                    ],
                    "correct_index": 0
                }
            ]
        },
        {
            "day_number": 6,
            "title": "Usability Testing, Heuristic Evaluation & Design Critiques",
            "subtopics": [
                (
                    "Nielsen Norman 10 Usability Heuristics",
                    "Evaluate interface designs against universally validated human-computer interaction heuristics.",
                    [
                        "Visibility of system status, feedback immediacy, and progress bars",
                        "Match between system and real world, error prevention, and user control (undo/redo)",
                        "Consistency, standards, recognition over recall, and minimalist aesthetics"
                    ]
                ),
                (
                    "Moderated & Unmoderated Usability Testing",
                    "Design testing protocols, recruit representative participants, and capture behavioral insights.",
                    [
                        "Writing neutral, unbiased task scenarios without leading questions",
                        "Think-aloud protocol execution during prototype testing sessions",
                        "Screen recording, heatmaps, clickstream analysis, and drop-off tracking"
                    ]
                ),
                (
                    "Quantitative UX Metrics & Synthesis",
                    "Measure user satisfaction and efficiency using standardized quantitative UX frameworks.",
                    [
                        "System Usability Scale (SUS) score calculation & benchmarking (>68 benchmark)",
                        "Task completion rate, Time-on-task, and Single Ease Question (SEQ)",
                        "Synthesizing qualitative feedback into affinity diagrams and prioritized UX backlogs"
                    ]
                )
            ],
            "quiz": [
                {
                    "id": 1,
                    "question": "Which usability heuristic is violated if a banking app performs a transfer but shows no confirmation dialog or loading indicator?",
                    "options": [
                        "Visibility of system status",
                        "Aesthetic and minimalist design",
                        "Flexibility and efficiency of use",
                        "Match between system and the real world"
                    ],
                    "correct_index": 0
                },
                {
                    "id": 2,
                    "question": "In standardized usability measurement, what SUS (System Usability Scale) score represents an above-average user experience?",
                    "options": [
                        "Above 68",
                        "Above 10",
                        "Exactly 50",
                        "Above 99 only"
                    ],
                    "correct_index": 0
                }
            ]
        },
        {
            "day_number": 7,
            "title": "Production Design Handoff, Spec Documentation & Developer Collaboration",
            "subtopics": [
                (
                    "Design-to-Code Handoff & Redline Documentation",
                    "Prepare pristine, production-ready Figma files equipped with developer annotations and specs.",
                    [
                        "Figma Dev Mode utilization: CSS, Swift, and Android Jetpack Compose code snippets",
                        "Explicit spatial redlines, padding tokens, and responsive behavior callouts",
                        "Defining component states (loading, empty, error, active, disabled) in handoff specs"
                    ]
                ),
                (
                    "Asset Optimization & Production Vector Hygiene",
                    "Export clean, scalable SVG assets and multi-resolution bitmaps optimized for web and mobile performance.",
                    [
                        "SVG path flattening, stroke outlining, and eliminating unnecessary vector nodes",
                        "WebP/AVIF raster formats and 1x/2x/3x resolution exports for mobile platforms",
                        "Icon font and SVG sprite compilation strategies"
                    ]
                ),
                (
                    "Design System Governance & Version Control",
                    "Establish ongoing design system maintenance, change management, and cross-functional syncs.",
                    [
                        "Semantic versioning for design systems (SemVer: major, minor, patch)",
                        "Component deprecation workflows, release notes, and migration guides",
                        "Collaborating seamlessly with engineering teams in sprint planning and QA audits"
                    ]
                )
            ],
            "quiz": [
                {
                    "id": 1,
                    "question": "Why should SVG icons have their strokes outlined and unnecessary groups flattened before developer export?",
                    "options": [
                        "To prevent stroke-width distortion when scaling and to minimize XML DOM file payload",
                        "To ensure the icon only renders in pure black and white",
                        "To convert the vector automatically into a low-resolution JPEG",
                        "To force the browser to cache the file in memory permanently"
                    ],
                    "correct_index": 0
                },
                {
                    "id": 2,
                    "question": "What is the primary objective of Figma Dev Mode during sprint execution?",
                    "options": [
                        "Bridge the gap between design tokens and production code with precise CSS, Swift, and Kotlin measurements",
                        "Allow developers to overwrite UI component colors without designer approval",
                        "Automatically run backend database migrations",
                        "Compile the entire application into a native desktop binary"
                    ],
                    "correct_index": 0
                }
            ]
        }
    ]
}


DEVOPS_CLOUD_COURSE = {
    "domain": "DevOps & Cloud",
    "title": "Cloud Infrastructure, Docker, Kubernetes & CI/CD Pipelines",
    "slug": "devops-cloud",
    "level": "Intermediate",
    "estimated_hours": 14,
    "banner_gradient": "linear-gradient(135deg, #0c4a6e 0%, #0369a1 50%, #0284c7 100%)",
    "chapters": [
        {
            "day_number": 1,
            "title": "Linux System Administration, Shell Scripting & Cloud Networking",
            "subtopics": [
                (
                    "Linux OS Internals, Permissions & Process Management",
                    "Master production Linux administration: POSIX permissions, systemd services, and resource monitoring.",
                    [
                        "File permissions (chmod, chown), setuid, and access control lists (ACLs)",
                        "Process monitoring (ps, top, htop), signals (SIGTERM, SIGKILL), and background jobs",
                        "Managing production systemd services, journalctl logs, and boot targets"
                    ]
                ),
                (
                    "Bash Scripting & Stream Processing (sed / awk / jq)",
                    "Automate operational tasks with robust Bash scripts, error trapping, and structured data parsing.",
                    [
                        "Defensive Bash scripting: set -euo pipefail, trap handlers, and exit codes",
                        "Text stream processing with grep, sed regular expressions, and awk tabular filtering",
                        "Parsing and manipulating JSON payloads in shell with jq"
                    ]
                ),
                (
                    "Cloud Networking Fundamentals: VPC, Subnets & CIDR",
                    "Architect secure cloud networking topologies with virtual private clouds and routing tables.",
                    [
                        "IPv4 CIDR block subnetting (/24, /16) and private vs public subnet partitioning",
                        "Internet Gateways (IGW), NAT Gateways, and Route Table propagation",
                        "Security Groups (stateful) vs Network Access Control Lists (NACLs - stateless)"
                    ]
                )
            ],
            "quiz": [
                {
                    "id": 1,
                    "question": "What is the primary difference between AWS Security Groups and Network ACLs (NACLs)?",
                    "options": [
                        "Security Groups are stateful (return traffic is automatically allowed); NACLs are stateless (rules must be defined in both directions)",
                        "Security Groups operate at the subnet level; NACLs operate at the instance level",
                        "Security Groups only filter outgoing traffic; NACLs only filter incoming traffic",
                        "Security Groups require software installation inside the Linux kernel; NACLs do not"
                    ],
                    "correct_index": 0
                },
                {
                    "id": 2,
                    "question": "What does the bash directive 'set -euo pipefail' accomplish in production automation scripts?",
                    "options": [
                        "Exits immediately on error, treats unset variables as errors, and preserves pipeline failure exit codes",
                        "Enables debug logging to standard output for every line executed",
                        "Automatically converts all shell commands to run in parallel in the background",
                        "Disables all network calls during script execution"
                    ],
                    "correct_index": 0
                }
            ]
        },
        {
            "day_number": 2,
            "title": "Containerization with Docker: Multi-Stage Builds, Images & Volumes",
            "subtopics": [
                (
                    "Container Virtualization vs Hypervisors & Docker Architecture",
                    "Understand Linux cgroups, namespaces, and union file systems that power lightweight container isolation.",
                    [
                        "Linux kernel namespaces (PID, NET, MNT, UTS) and cgroup resource quotas",
                        "Docker daemon architecture, containerd, and OCI image specifications",
                        "Container lifecycle: create, start, stop, restart, pause, and prune"
                    ]
                ),
                (
                    "Writing Production Dockerfiles & Multi-Stage Builds",
                    "Construct hardened, minimal container images by decoupling build toolchains from runtime containers.",
                    [
                        "Multi-stage build pipelines: compiling binaries in builder stages, copying to alpine/distroless",
                        "Layer caching optimization: ordering package installation and dependency manifests first",
                        "Non-root user execution (USER appuser) and minimizing CVE attack surface"
                    ]
                ),
                (
                    "Container Storage, Volume Persistence & Networking",
                    "Manage persistent state and inter-container communication using Docker volume and bridge networks.",
                    [
                        "Docker named volumes vs host bind mounts for database persistence",
                        "User-defined bridge networks with automatic DNS container discovery",
                        "Port mapping (-p host:container) and environment variable injection"
                    ]
                )
            ],
            "quiz": [
                {
                    "id": 1,
                    "question": "Why are multi-stage Docker builds recommended for production microservices?",
                    "options": [
                        "They separate heavy build compilers from final images, producing drastically smaller and more secure runtime images",
                        "They allow a single Dockerfile to run on Windows, Mac, and Linux simultaneously without Docker installed",
                        "They run container processes with root privileges for maximum execution speed",
                        "They eliminate the need for container volume storage"
                    ],
                    "correct_index": 0
                },
                {
                    "id": 2,
                    "question": "Which Linux kernel feature enables Docker to enforce CPU and RAM limits on a container?",
                    "options": [
                        "cgroups (Control Groups)",
                        "PID Namespaces",
                        "iptables",
                        "SELinux"
                    ],
                    "correct_index": 0
                }
            ]
        },
        {
            "day_number": 3,
            "title": "Docker Compose, Microservices Orchestration & Reverse Proxying",
            "subtopics": [
                (
                    "Multi-Service Orchestration with Docker Compose",
                    "Define, spin up, and manage connected application stacks consisting of web apps, databases, and caches.",
                    [
                        "compose.yaml syntax: services, networks, volumes, and depends_on health conditions",
                        "Environment variable interpolation via .env files",
                        "Resource reservation, restart policies, and logging drivers"
                    ]
                ),
                (
                    "Reverse Proxying & SSL Termination with Nginx",
                    "Configure high-performance Nginx proxies for load distribution, SSL/TLS certificates, and caching.",
                    [
                        "Upstream server definitions and round-robin load distribution",
                        "SSL/TLS termination, HTTP/2 enforcement, and Let's Encrypt Certbot automation",
                        "Gzip compression, client max body size, and security headers (HSTS, CSP)"
                    ]
                ),
                (
                    "Container Health Checks, Logging & Graceful Teardowns",
                    "Ensure service availability with proactive health probes and non-disruptive rolling reboots.",
                    [
                        "Defining Docker HEALTHCHECK directives with curl/wget probes",
                        "Docker logging drivers (json-file, syslog) with log rotation limits",
                        "Handling SIGTERM and SIGINT signals for graceful backend connection draining"
                    ]
                )
            ],
            "quiz": [
                {
                    "id": 1,
                    "question": "In a Docker Compose file, how do services on the same default user-defined network communicate with each other?",
                    "options": [
                        "By using the service name as the hostname via Docker's internal DNS resolver",
                        "By hardcoding the host machine's public IP address",
                        "By writing data to a shared temporary text file",
                        "By opening SSH connections between containers"
                    ],
                    "correct_index": 0
                },
                {
                    "id": 2,
                    "question": "What is the primary role of a reverse proxy like Nginx in front of application containers?",
                    "options": [
                        "Handle SSL termination, request routing, static file caching, and protect internal application ports",
                        "Compile frontend React and Next.js applications in real time",
                        "Act as a relational database storage engine",
                        "Generate automated unit tests for backend APIs"
                    ],
                    "correct_index": 0
                }
            ]
        },
        {
            "day_number": 4,
            "title": "Infrastructure as Code (IaC) with Terraform & AWS Core Architecture",
            "subtopics": [
                (
                    "Declarative IaC Principles & HashiCorp HCL Syntax",
                    "Provision immutable cloud infrastructure through code using declarative configurations.",
                    [
                        "Terraform workflow: init, plan, apply, and destroy",
                        "HCL syntax: resource blocks, data sources, input variables, and output values",
                        "Terraform providers, version pinning, and module reusability"
                    ]
                ),
                (
                    "State Management, Remote Backends & State Locking",
                    "Collaborate securely on infrastructure by storing Terraform state remotely with concurrency locks.",
                    [
                        "The critical role of terraform.tfstate: mapping configuration to real-world cloud resources",
                        "Configuring Amazon S3 remote state backends with encryption-at-rest",
                        "DynamoDB table state locking to prevent concurrent destructive operations"
                    ]
                ),
                (
                    "Provisioning Scalable Cloud Infrastructure on AWS",
                    "Write production Terraform configurations to spin up hardened VPCs, EC2 instances, and RDS databases.",
                    [
                        "Provisioning custom VPC, public/private subnets, and internet gateways",
                        "EC2 instance launch configurations, key pairs, and user_data bootstrap scripts",
                        "PostgreSQL RDS instance provisioning with automated backups and security groups"
                    ]
                )
            ],
            "quiz": [
                {
                    "id": 1,
                    "question": "Why is remote state locking with a tool like DynamoDB critical when using Terraform in team environments?",
                    "options": [
                        "It prevents two engineers from executing simultaneous applies that could corrupt cloud state",
                        "It speeds up EC2 instance boot time by caching operating system kernels",
                        "It automatically converts HCL syntax into Python code",
                        "It eliminates the cost of AWS cloud infrastructure"
                    ],
                    "correct_index": 0
                },
                {
                    "id": 2,
                    "question": "What does 'terraform plan' do before applying infrastructure changes?",
                    "options": [
                        "Creates an execution spec showing exact additions, modifications, and deletions without modifying live resources",
                        "Immediately deletes existing cloud infrastructure and restarts from scratch",
                        "Generates automated invoices and charges credit cards",
                        "Scans application code for syntax errors and unit test failures"
                    ],
                    "correct_index": 0
                }
            ]
        },
        {
            "day_number": 5,
            "title": "Kubernetes Architecture: Pods, Deployments, Services & Ingress Controllers",
            "subtopics": [
                (
                    "Kubernetes Control Plane & Node Architecture",
                    "Understand master node components (API Server, etcd, Scheduler, Controller Manager) and worker nodes.",
                    [
                        "Control plane architecture: kube-apiserver, etcd key-value store, kube-scheduler",
                        "Worker node components: kubelet, kube-proxy, and container runtime interface (CRI)",
                        "kubectl command line mastery: context switching, namespaces, and object inspection"
                    ]
                ),
                (
                    "Declarative Pods, Deployments & Rolling Updates",
                    "Manage containerized workloads using declarative manifests, replica sets, and zero-downtime updates.",
                    [
                        "Pod anatomy: containers, initContainers, resource requests, and limits",
                        "Deployment specs, replica counts, and rolling update strategies (maxSurge, maxUnavailable)",
                        "Liveness, Readiness, and Startup probes to protect routing from unready containers"
                    ]
                ),
                (
                    "Services, Ingress Controllers & ConfigMaps",
                    "Expose workloads securely to internal and external traffic while managing environment configurations.",
                    [
                        "ClusterIP, NodePort, and LoadBalancer service abstractions",
                        "Ingress resources and Nginx Ingress Controller path-based and host-based routing",
                        "Decoupling application config and secrets using ConfigMaps and Kubernetes Secrets"
                    ]
                )
            ],
            "quiz": [
                {
                    "id": 1,
                    "question": "In Kubernetes, what is the role of a Readiness Probe on a Pod?",
                    "options": [
                        "Determines if a container is ready to accept user traffic; if failing, removes the Pod from Service endpoints",
                        "Reboots the entire Kubernetes worker node when CPU exceeds 90%",
                        "Compiles Java and Go code inside the Pod before runtime",
                        "Checks whether git commit messages follow conventional commit rules"
                    ],
                    "correct_index": 0
                },
                {
                    "id": 2,
                    "question": "Which component is the consistent, highly-available key-value data store for all cluster state in Kubernetes?",
                    "options": [
                        "etcd",
                        "kube-proxy",
                        "Redis",
                        "kube-scheduler"
                    ],
                    "correct_index": 0
                }
            ]
        },
        {
            "day_number": 6,
            "title": "Automated CI/CD Pipelines with GitHub Actions & Automated Testing",
            "subtopics": [
                (
                    "CI/CD Pipeline Architecture & GitHub Actions Workflows",
                    "Design automated delivery pipelines triggering on pull requests, merges, and semantic tags.",
                    [
                        "Workflow triggers: push, pull_request, release, and workflow_dispatch",
                        "Jobs, runner environments (ubuntu-latest), steps, actions, and dependency matrices",
                        "Secure secret management with GitHub Repository Secrets and OIDC cloud authentication"
                    ]
                ),
                (
                    "Automated Testing, Linting & Container Image Publishing",
                    "Ensure code quality and publish hardened container artifacts to container registries automatically.",
                    [
                        "Running unit, integration, and security scans (Trivy, SonarQube) in parallel jobs",
                        "Building multi-platform Docker images with docker/build-push-action and QEMU",
                        "Pushing tagged images to GitHub Packages (GHCR) or AWS ECR with immutable digest SHA tags"
                    ]
                ),
                (
                    "Automated Cloud Deployment & Rollback Mechanisms",
                    "Deploy code seamlessly to cloud hosts and implement automated health-verified rollbacks.",
                    [
                        "SSH deployment automation: executing remote docker pull and systemctl service reload",
                        "Kubernetes continuous deployment: kubectl set image / Helm upgrade in CI/CD",
                        "Smoke testing deployed endpoints and automated rollback triggers upon failure"
                    ]
                )
            ],
            "quiz": [
                {
                    "id": 1,
                    "question": "Why should container images in CI/CD pipelines be tagged with git commit SHAs rather than relying solely on ':latest'?",
                    "options": [
                        "Commit SHAs provide immutable, traceable artifacts ensuring reproducible deployments and easy rollbacks",
                        "The ':latest' tag is deprecated and no longer supported by Docker registry servers",
                        "Commit SHAs automatically compress container disk sizes by 50%",
                        "Tagged images with SHAs bypass all operating system security checks"
                    ],
                    "correct_index": 0
                },
                {
                    "id": 2,
                    "question": "In GitHub Actions, how do you prevent production deployment jobs from running if automated test jobs fail?",
                    "options": [
                        "Use the 'needs: [test-job-name]' directive on the deployment job",
                        "Place deployment steps inside the README.md file",
                        "Set 'continue-on-error: true' on all testing steps",
                        "Delete the test runner after the job begins"
                    ],
                    "correct_index": 0
                }
            ]
        },
        {
            "day_number": 7,
            "title": "Cloud Observability, Prometheus, Grafana, Log Aggregation & Incident Response",
            "subtopics": [
                (
                    "The Three Pillars of Observability: Metrics, Logs & Traces",
                    "Establish comprehensive system visibility across distributed microservice architectures.",
                    [
                        "Understanding metrics (counters, gauges, histograms), structured logs, and distributed traces",
                        "Instrumentation with OpenTelemetry and exporting telemetry data to collectors",
                        "Distinguishing proactive monitoring from reactive symptom checking"
                    ]
                ),
                (
                    "Metrics Scraping with Prometheus & Grafana Dashboards",
                    "Deploy and query time-series monitoring systems to track CPU, memory, latency, and error rates.",
                    [
                        "Prometheus pull-model metrics architecture and Node Exporter / cAdvisor setup",
                        "Writing PromQL queries: rate(), irate(), histogram_quantile(), and aggregation operators",
                        "Constructing real-time Grafana dashboards with executive health cards and alerts"
                    ]
                ),
                (
                    "Centralized Logging, Alerting Rules & Incident Response",
                    "Aggregate distributed system logs, configure automated alert thresholds, and manage on-call incidents.",
                    [
                        "Centralized log shipping with Promtail/Loki or Filebeat/Elasticsearch",
                        "Configuring Prometheus Alertmanager with Slack, PagerDuty, and Email notification channels",
                        "Defining Service Level Objectives (SLOs), Service Level Indicators (SLIs), and Error Budgets"
                    ]
                )
            ],
            "quiz": [
                {
                    "id": 1,
                    "question": "In time-series metrics monitoring with Prometheus, which PromQL function calculates the per-second average rate of increase of a counter over a specified time window?",
                    "options": [
                        "rate()",
                        "sum()",
                        "count()",
                        "avg_over_time()"
                    ],
                    "correct_index": 0
                },
                {
                    "id": 2,
                    "question": "What is the primary difference between a Service Level Indicator (SLI) and a Service Level Objective (SLO)?",
                    "options": [
                        "An SLI is a quantifiable metric of service performance (e.g. 99.2% success); an SLO is the target goal agreed upon (e.g. 99.9% uptime)",
                        "An SLI is an internal document; an SLO is the legal contract signed with paying customers",
                        "SLIs are measured in dollars; SLOs are measured in gigabytes",
                        "SLIs only apply to hardware servers; SLOs only apply to software applications"
                    ],
                    "correct_index": 0
                }
            ]
        }
    ]
}


MOBILE_APP_DEVELOPMENT_COURSE = {
    "domain": "Mobile App Development",
    "title": "Cross-Platform Mobile App Engineering with React Native & Expo",
    "slug": "mobile-app-development",
    "level": "Intermediate",
    "estimated_hours": 14,
    "banner_gradient": "linear-gradient(135deg, #14532d 0%, #15803d 50%, #16a34a 100%)",
    "chapters": [
        {
            "day_number": 1,
            "title": "Mobile Architecture, React Native Runtime & Expo Workflow Setup",
            "subtopics": [
                (
                    "React Native Architecture: JS Thread, Shadow Tree & Fabric",
                    "Understand how React Native executes JavaScript logic and renders 100% native UI widgets.",
                    [
                        "The New Architecture: Hermes JS Engine, JSI (JavaScript Interface) & Fabric Renderer",
                        "Comparison between hybrid WebViews, Flutter canvas rendering, and React Native native bridges",
                        "UI Thread (60/120 FPS) vs JavaScript Thread performance decoupling"
                    ]
                ),
                (
                    "Expo Ecosystem: Managed Workflow & Development Builds",
                    "Set up cross-platform developer toolchains utilizing Expo SDK and Expo Go simulators.",
                    [
                        "Expo Managed Workflow vs Bare React Native native codebases",
                        "Configuring app.json, bundle identifiers, and platform permissions",
                        "Running on physical iOS/Android hardware via Expo Go and development clients"
                    ]
                ),
                (
                    "Project Structure, TypeScript & Environment Setup",
                    "Structure a scalable production mobile codebase with strict TypeScript typing and environment variables.",
                    [
                        "Folder architecture: screens, components, hooks, services, navigation, and theme",
                        "Strict TypeScript interfaces for component props, navigation routes, and API responses",
                        "Environment configuration with react-native-dotenv and Expo Config Plugins"
                    ]
                )
            ],
            "quiz": [
                {
                    "id": 1,
                    "question": "How does React Native achieve native performance compared to WebView-based mobile frameworks?",
                    "options": [
                        "It renders genuine platform native UI components (UIKit on iOS, Android Views on Android) instead of running inside a web browser",
                        "It compiles all JavaScript directly into pure C++ machine code before installing on the device",
                        "It executes all app code on remote cloud servers rather than on the phone hardware",
                        "It disables all device background services to preserve battery life"
                    ],
                    "correct_index": 0
                },
                {
                    "id": 2,
                    "question": "What is the primary role of the Hermes engine in modern React Native applications?",
                    "options": [
                        "An optimized, lightweight JavaScript engine designed specifically for fast Android/iOS mobile startup time and low memory footprint",
                        "A database engine for storing local SQLite tables",
                        "A cloud compiler that uploads apps directly to the Apple App Store",
                        "A graphic design tool for vector iconography"
                    ],
                    "correct_index": 0
                }
            ]
        },
        {
            "day_number": 2,
            "title": "Core Components, Flexbox Layouts & Responsive Mobile Styling",
            "subtopics": [
                (
                    "React Native Core Primitives (View, Text, ScrollView, Pressable)",
                    "Master mobile layout primitives, touch feedback, and text rendering rules across iOS and Android.",
                    [
                        "Why raw text must always be wrapped in <Text> components",
                        "Handling touch with <Pressable> and custom hitSlop hit areas",
                        "Virtualizing long lists with <FlatList> and <SectionList> instead of <ScrollView>"
                    ]
                ),
                (
                    "Mobile Flexbox Layouts & Dimensional Adaptation",
                    "Build responsive mobile interfaces accommodating diverse screen aspect ratios, notches, and safe areas.",
                    [
                        "Flexbox differences in React Native: flexDirection defaults to 'column'",
                        "Managing device notches and home indicator bars with react-native-safe-area-context",
                        "useWindowDimensions hook and dynamic responsive percentage scaling"
                    ]
                ),
                (
                    "Design Tokens, Dark Mode & Theme Providers",
                    "Implement scalable styling systems supporting dynamic device theme changes and accessibility text scaling.",
                    [
                        "StyleSheet.create benefits: validation, optimization, and ID registration",
                        "Light and Dark mode support with useColorScheme() hook",
                        "Accounting for user system font accessibility scaling (allowFontScaling considerations)"
                    ]
                )
            ],
            "quiz": [
                {
                    "id": 1,
                    "question": "In React Native Flexbox, what is the default value of 'flexDirection'?",
                    "options": [
                        "column",
                        "row",
                        "row-reverse",
                        "wrap"
                    ],
                    "correct_index": 0
                },
                {
                    "id": 2,
                    "question": "Why should <FlatList> be used instead of <ScrollView> for displaying large collections of items (e.g. 500 items)?",
                    "options": [
                        "FlatList virtualizes offscreen items, rendering only visible elements to conserve device memory and maintain 60 FPS",
                        "FlatList automatically downloads images from the internet without network calls",
                        "ScrollView is deprecated and throws fatal errors in React Native",
                        "FlatList eliminates the need for component state"
                    ],
                    "correct_index": 0
                }
            ]
        },
        {
            "day_number": 3,
            "title": "Navigation Architectures: Stacks, Tabs, Drawers & Deep Linking",
            "subtopics": [
                (
                    "React Navigation: Native Stack & Tab Navigator Setup",
                    "Implement standard mobile navigation patterns using native platform transitions.",
                    [
                        "@react-navigation/native-stack utilizing platform-native screen transition animations",
                        "@react-navigation/bottom-tabs for persistent bottom navigation bars",
                        "Customizing header bars, back buttons, and tab icon badges"
                    ]
                ),
                (
                    "Nested Navigators & Strongly-Typed Route Parameters",
                    "Structure complex multi-tier navigation hierarchies with type-safe parameters.",
                    [
                        "Nesting Stack Navigators inside Bottom Tabs and Modal overlays",
                        "Passing strongly-typed parameters with NativeStackScreenProps",
                        "Handling authentication state: conditional auth switch vs authenticated stack"
                    ]
                ),
                (
                    "Deep Linking, Universal Links & URL Routing",
                    "Enable external URLs and push notifications to route users directly into deep app screens.",
                    [
                        "Configuring custom URL schemes (e.g. dbert://course/12)",
                        "Linking configuration object mapping pathnames to screens",
                        "Handling universal links (HTTPS domain verification on iOS and Android)"
                    ]
                )
            ],
            "quiz": [
                {
                    "id": 1,
                    "question": "What is the primary architectural advantage of using '@react-navigation/native-stack' over the JS-based '@react-navigation/stack'?",
                    "options": [
                        "Native stack uses platform-native UI navigation primitives (UINavigationController on iOS, Fragment on Android) for smoother 60/120 FPS transitions",
                        "Native stack does not require React code",
                        "Native stack automatically translates the entire application into C++",
                        "Native stack bypasses all mobile security sandboxes"
                    ],
                    "correct_index": 0
                },
                {
                    "id": 2,
                    "question": "How should conditional authentication routing (e.g. Login vs Main App) be managed in modern React Navigation?",
                    "options": [
                        "Conditionally render either the Auth Stack or App Stack based on authentication state in the root Navigator",
                        "Call navigation.navigate() in an infinite useEffect loop until login occurs",
                        "Hardcode user passwords directly inside the screen components",
                        "Force the phone to restart every time the user signs out"
                    ],
                    "correct_index": 0
                }
            ]
        },
        {
            "day_number": 4,
            "title": "Mobile State Management, Async Storage & Offline Data Persistence",
            "subtopics": [
                (
                    "Global State Management for Mobile (Zustand & Context API)",
                    "Manage client application state across screens without unnecessary component re-renders.",
                    [
                        "Lightweight mobile state management using Zustand stores",
                        "Selective subscriptions to prevent re-rendering entire screen trees",
                        "Managing user session tokens, theme preferences, and cart states"
                    ]
                ),
                (
                    "Encrypted Storage & Local Device Persistence",
                    "Store persistent data on the mobile file system using secure keychains and key-value stores.",
                    [
                        "AsyncStorage for non-sensitive cached configurations and preferences",
                        "Expo SecureStore / react-native-keychain for encrypted auth tokens and biometric credentials",
                        "Local relational database caching with expo-sqlite for offline document records"
                    ]
                ),
                (
                    "Offline-First Architecture & Data Synchronization",
                    "Engineer resilient apps that function seamlessly offline and sync changes upon reconnection.",
                    [
                        "Detecting network connectivity status with @react-native-community/netinfo",
                        "Queuing offline mutations in local storage queues",
                        "Optimistic UI updates and resolving merge conflicts upon reconnection"
                    ]
                )
            ],
            "quiz": [
                {
                    "id": 1,
                    "question": "Where should sensitive credentials like authentication JWT tokens or API secrets be stored on a mobile device?",
                    "options": [
                        "Expo SecureStore / Hardware Keychain (iOS Keychain / Android Keystore)",
                        "Unencrypted AsyncStorage text files",
                        "Global JavaScript window variables",
                        "Embedded inside public images in the assets folder"
                    ],
                    "correct_index": 0
                },
                {
                    "id": 2,
                    "question": "In an offline-first mobile application, what is an 'optimistic UI update'?",
                    "options": [
                        "Updating the screen interface immediately as if the network request succeeded, then syncing in background or rolling back on error",
                        "Showing a blocking full-screen loading spinner until the user connects to high-speed WiFi",
                        "Assuming the user will always have 5G network coverage",
                        "Deleting local data if the server fails to respond within 1 second"
                    ],
                    "correct_index": 0
                }
            ]
        },
        {
            "day_number": 5,
            "title": "Device Hardware APIs: Camera, Geolocation, Sensors & Biometrics",
            "subtopics": [
                (
                    "Camera, Media Library & Image Uploads",
                    "Capture photos, select gallery assets, and prepare media for cloud upload.",
                    [
                        "Requesting runtime permissions with expo-camera and expo-image-picker",
                        "Image compression, resizing, and aspect ratio constraints before network upload",
                        "Generating multipart/form-data payloads from local file URIs"
                    ]
                ),
                (
                    "Geolocation, Maps & Background Location Tracking",
                    "Access GPS location sensors, render interactive maps, and handle battery-efficient geofences.",
                    [
                        "Requesting foreground vs background location permissions (expo-location)",
                        "Rendering interactive map pins, callouts, and polylines with react-native-maps",
                        "Battery conservation strategies: distance intervals and accuracy thresholds"
                    ]
                ),
                (
                    "Biometric Authentication & Haptic Feedback",
                    "Enhance user security and tactile interaction with hardware fingerprint/FaceID sensors and haptics.",
                    [
                        "Enrolling and authenticating with FaceID / TouchID using expo-local-authentication",
                        "Providing tactile user feedback on key interactions with expo-haptics (light, medium, success)",
                        "Fallback authentication mechanisms for devices without biometric hardware"
                    ]
                )
            ],
            "quiz": [
                {
                    "id": 1,
                    "question": "Why must mobile image uploads from camera rolls always be resized or compressed before transmission to backend APIs?",
                    "options": [
                        "Modern mobile cameras produce 10-25MB photos which consume excessive cellular data, device RAM, and cause upload timeouts",
                        "Web servers reject any image that has more than 2 colors",
                        "React Native cannot open files larger than 100 kilobytes",
                        "Operating systems automatically block uncompressed photos from leaving the device"
                    ],
                    "correct_index": 0
                },
                {
                    "id": 2,
                    "question": "When requesting hardware permissions (e.g. Camera or GPS Location) on mobile devices, what is the best UX practice?",
                    "options": [
                        "Explain why the permission is needed in context right before requesting the system permission prompt",
                        "Request every possible device permission simultaneously upon initial app launch before the user sees any screen",
                        "Silently bypass system permission checks using private APIs",
                        "Crash the app if the user denies camera permission on first prompt"
                    ],
                    "correct_index": 0
                }
            ]
        },
        {
            "day_number": 6,
            "title": "REST & GraphQL API Integration, Image Caching & Push Notifications",
            "subtopics": [
                (
                    "Consuming REST & GraphQL APIs with TanStack React Query",
                    "Build reliable data-fetching layers with automated caching, pagination, and retry logic.",
                    [
                        "Axios instance configuration with request/response interceptors for auth headers",
                        "Server-state management with TanStack React Query: query keys, staleTime, and refetchOnWindowFocus",
                        "Infinite scroll pagination with fetchNextPage and FlatList onEndReached"
                    ]
                ),
                (
                    "Image Caching Strategies & Memory Footprint Optimization",
                    "Prevent image flicker and memory leaks using dedicated native image caching solutions.",
                    [
                        "Utilizing expo-image with SDWebImage (iOS) and Glide (Android) native caching backends",
                        "Progressive image loading, blurhash placeholders, and memory footprint management",
                        "Vector icons integration with @expo/vector-icons without bloating APK/IPA bundle size"
                    ]
                ),
                (
                    "Push Notifications Architecture with FCM & APNs",
                    "Implement remote and local push notifications to re-engage users across iOS and Android.",
                    [
                        "Push notification architecture: APNs (Apple) & Firebase Cloud Messaging (Android)",
                        "Obtaining device push tokens using expo-notifications",
                        "Handling foreground notifications, background taps, and payload routing"
                    ]
                )
            ],
            "quiz": [
                {
                    "id": 1,
                    "question": "What is the primary benefit of using a specialized image component like 'expo-image' instead of the basic React Native <Image> component?",
                    "options": [
                        "It leverages high-performance native caching libraries (SDWebImage / Glide), supports BlurHash placeholders, and minimizes memory leaks",
                        "It automatically translates text inside images into English",
                        "It converts JPEG images into vector animations",
                        "It generates AI images directly on the user's phone without an API key"
                    ],
                    "correct_index": 0
                },
                {
                    "id": 2,
                    "question": "How do remote push notifications reach an iPhone when the application is completely closed (not running in background)?",
                    "options": [
                        "The notification is sent via Apple Push Notification service (APNs), which the iOS operating system listens to persistently and displays on screen",
                        "The app continuously runs in the background at 100% CPU usage",
                        "The backend server sends direct SMS text messages to the SIM card",
                        "Push notifications cannot be received if an application is closed"
                    ],
                    "correct_index": 0
                }
            ]
        },
        {
            "day_number": 7,
            "title": "Mobile Performance Optimization, Release Builds & App Store / Play Store Deployment",
            "subtopics": [
                (
                    "Performance Profiling, Re-Render Elimination & Memory Hygiene",
                    "Profile mobile apps using React DevTools, Flipper, and Hermes memory profilers.",
                    [
                        "Identifying unnecessary re-renders with React.memo, useCallback, and useMemo",
                        "FlatList optimization: getItemLayout, windowSize, and removeClippedSubviews",
                        "Investigating memory leaks and native bridge traffic bottlenecks"
                    ]
                ),
                (
                    "Android Production Builds (AAB) & Keystore Signing",
                    "Build optimized Android App Bundles (AAB), configure ProGuard shrinking, and sign with release keystores.",
                    [
                        "Generating upload keystores and configuring Gradle signingConfigs",
                        "ProGuard and R8 code shrinking and resource obfuscation",
                        "Building AAB binaries using EAS Build (Expo Application Services) or local Gradle assembleRelease"
                    ]
                ),
                (
                    "iOS Production Distribution & App Store Review Preparation",
                    "Package iOS IPAs, manage certificates and provisioning profiles, and navigate App Store Review guidelines.",
                    [
                        "Apple Developer Program: App IDs, Distribution Certificates & Provisioning Profiles",
                        "Automating test builds with TestFlight for internal and external beta distribution",
                        "App Store Review guidelines compliance: privacy policy, account deletion, and in-app purchase rules"
                    ]
                )
            ],
            "quiz": [
                {
                    "id": 1,
                    "question": "Why does Google Play require Android App Bundles (.aab) instead of monolithic APK (.apk) files for new apps?",
                    "options": [
                        "Google Play uses the App Bundle to dynamically generate and serve optimized APKs tailored to each user's specific device architecture and screen density",
                        "AAB files can be executed on iPhones and iPads directly",
                        "AAB files do not require any code signing or certificates",
                        "Monolithic APKs are limited to a maximum size of 1 megabyte"
                    ],
                    "correct_index": 0
                },
                {
                    "id": 2,
                    "question": "When optimizing a React Native FlatList displaying hundreds of complex items, which prop improves scroll performance by skipping layout measurement for fixed-height rows?",
                    "options": [
                        "getItemLayout",
                        "horizontal",
                        "inverted",
                        "pagingEnabled"
                    ],
                    "correct_index": 0
                }
            ]
        }
    ]
}


CYBERSECURITY_COURSE = {
    "domain": "Cybersecurity",
    "title": "Offensive & Defensive Cybersecurity, SOC Analysis & Threat Modeling",
    "slug": "cybersecurity",
    "level": "Intermediate",
    "estimated_hours": 14,
    "banner_gradient": "linear-gradient(135deg, #7f1d1d 0%, #b91c1c 50%, #dc2626 100%)",
    "chapters": [
        {
            "day_number": 1,
            "title": "Security Fundamentals, The CIA Triad, OSI Model & Network Packet Analysis",
            "subtopics": [
                (
                    "The CIA Triad & Core Information Security Tenets",
                    "Establish security foundations across Confidentiality, Integrity, Availability, and Defense-in-Depth.",
                    [
                        "Confidentiality (encryption, access controls), Integrity (hashing, signatures), Availability (redundancy, DDoS defense)",
                        "Authentication vs Authorization: RBAC, ABAC, and Principle of Least Privilege",
                        "Defense-in-Depth: layered security across network, host, application, and data tiers"
                    ]
                ),
                (
                    "Network Architecture, Protocols & OSI Layer Vulnerabilities",
                    "Analyze TCP/IP and OSI stack vulnerabilities across packet headers, ARP, DNS, and IP routing.",
                    [
                        "OSI 7 layers and typical security threats per layer (ARP poisoning, SYN floods, DNS spoofing)",
                        "TCP 3-way handshake mechanics (SYN, SYN-ACK, ACK) and connection teardowns",
                        "Common network service ports: SSH (22), DNS (53), HTTP/S (80/443), RDP (3389)"
                    ]
                ),
                (
                    "Network Traffic Inspection with Wireshark & TShark",
                    "Capture, dissect, and analyze raw network traffic to detect reconnaissance probes and cleartext data leaks.",
                    [
                        "Capturing packets on network interfaces using Wireshark and tcpdump",
                        "Display filters for isolating suspicious protocol traffic (e.g. tcp.flags.syn==1 && tcp.flags.ack==0)",
                        "Extracting credentials and inspecting unencrypted protocols (HTTP, FTP, Telnet)"
                    ]
                )
            ],
            "quiz": [
                {
                    "id": 1,
                    "question": "Which pillar of the CIA Triad is directly violated when an attacker performs a cryptographic hash collision attack on a software update binary?",
                    "options": [
                        "Integrity",
                        "Confidentiality",
                        "Availability",
                        "Non-repudiation"
                    ],
                    "correct_index": 0
                },
                {
                    "id": 2,
                    "question": "In a TCP SYN Flood attack, which vulnerability in the TCP connection lifecycle does the adversary exploit?",
                    "options": [
                        "Sending numerous SYN packets without completing the 3-way handshake with an ACK, exhausting server connection backlogs",
                        "Cracking the AES-256 encryption key on the SSL certificate",
                        "Modifying the physical Ethernet MAC address on the client network card",
                        "Overwriting the DNS zone records on the root nameserver"
                    ],
                    "correct_index": 0
                }
            ]
        },
        {
            "day_number": 2,
            "title": "Threat Modeling, Attack Surfaces & The MITRE ATT&CK Framework",
            "subtopics": [
                (
                    "Threat Modeling Frameworks: STRIDE, DREAD & PASTA",
                    "Identify architectural vulnerabilities proactively during application design before writing code.",
                    [
                        "STRIDE threat categorization: Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege",
                        "Risk rating methodologies: DREAD (Damage, Reproducibility, Exploitability, Affected Users, Discoverability)",
                        "Creating Data Flow Diagrams (DFDs) with trust boundaries and attack surface enumeration"
                    ]
                ),
                (
                    "The MITRE ATT&CK Framework & Adversary Tactics",
                    "Map adversary techniques, procedures, and tactics across enterprise attack matrices.",
                    [
                        "Enterprise ATT&CK matrix: Initial Access, Execution, Persistence, Privilege Escalation, Defense Evasion, Exfiltration",
                        "Understanding TTPs (Tactics, Techniques, and Procedures) and adversary profiling",
                        "Mapping specific threat group signatures (APTs) to organizational defensive controls"
                    ]
                ),
                (
                    "The Cyber Kill Chain & Attack Surface Reduction",
                    "Deconstruct adversary engagement stages and eliminate exposed attack vectors.",
                    [
                        "Lockheed Martin Cyber Kill Chain: Recon, Weaponization, Delivery, Exploitation, Installation, C2, Actions on Objectives",
                        "Disabling unnecessary network protocols, ports, and default credentials",
                        "Continuous external attack surface management (EASM) and asset discovery"
                    ]
                )
            ],
            "quiz": [
                {
                    "id": 1,
                    "question": "Under the STRIDE threat modeling framework, which threat type involves an attacker modifying balance ledger rows directly in a database?",
                    "options": [
                        "Tampering",
                        "Repudiation",
                        "Denial of Service",
                        "Information Disclosure"
                    ],
                    "correct_index": 0
                },
                {
                    "id": 2,
                    "question": "What is the primary operational purpose of the MITRE ATT&CK framework for security teams?",
                    "options": [
                        "Provide a comprehensive, globally-accessible knowledge base of real-world adversary tactics and techniques to benchmark defenses",
                        "Serve as an open-source antivirus scanner for consumer laptops",
                        "Act as a programming language for writing web applications",
                        "Replace all hardware firewalls with cloud software"
                    ],
                    "correct_index": 0
                }
            ]
        },
        {
            "day_number": 3,
            "title": "Web Application Security & OWASP Top 10 Exploitation/Mitigation",
            "subtopics": [
                (
                    "Injection Vulnerabilities: SQLi, NoSQLi & Command Injection",
                    "Understand how unvalidated user input corrupts query execution and learn parameterized defenses.",
                    [
                        "SQL Injection mechanics: Classic in-band, Error-based, and Blind boolean/time-based injection",
                        "OS Command Injection via unsanitized subprocess calls",
                        "Definitive mitigation: Parameterized prepared statements, ORM boundaries, and strict input validation"
                    ]
                ),
                (
                    "Cross-Site Scripting (XSS), CSRF & Modern Browser Defenses",
                    "Analyze client-side exploitation vectors and enforce strict browser execution controls.",
                    [
                        "Stored, Reflected, and DOM-based Cross-Site Scripting (XSS)",
                        "Cross-Site Request Forgery (CSRF) mechanics and SameSite cookie protections",
                        "Content Security Policy (CSP) headers, nonce enforcement, and Subresource Integrity (SRI)"
                    ]
                ),
                (
                    "Broken Access Control, IDOR & JWT Security Pitfalls",
                    "Identify authorization flaws allowing unauthorized data manipulation and account takeover.",
                    [
                        "Insecure Direct Object References (IDOR): manipulating user IDs in URL parameters",
                        "JSON Web Token (JWT) vulnerabilities: algorithm confusion ('none'), weak HMAC secrets, and replay attacks",
                        "Server-side authorization enforcement on every single API endpoint"
                    ]
                )
            ],
            "quiz": [
                {
                    "id": 1,
                    "question": "What is the single most effective technical defense against SQL Injection vulnerabilities?",
                    "options": [
                        "Using parameterized prepared statements (bind variables) so user input is never interpreted as executable SQL syntax",
                        "Replacing single quotes with double quotes in application memory",
                        "Running web applications on Linux instead of Windows servers",
                        "Installing a larger hard drive on the database server"
                    ],
                    "correct_index": 0
                },
                {
                    "id": 2,
                    "question": "What does a Content Security Policy (CSP) HTTP response header accomplish?",
                    "options": [
                        "Restricts the domains from which scripts, styles, images, and other resources can be loaded and executed by the browser",
                        "Encrypts all database tables at rest using AES-256",
                        "Forces users to change their passwords every 30 days",
                        "Blocks search engines from indexing private web pages"
                    ],
                    "correct_index": 0
                }
            ]
        },
        {
            "day_number": 4,
            "title": "Cryptographic Protocols, PKI, Symmetric/Asymmetric Ciphers & TLS",
            "subtopics": [
                (
                    "Symmetric & Asymmetric Cryptography Fundamentals",
                    "Master cryptographic building blocks: block ciphers, public-key pairs, and key exchange mathematics.",
                    [
                        "Symmetric ciphers: AES-GCM (Galois/Counter Mode) with authenticated encryption and IV nonces",
                        "Asymmetric ciphers: RSA and Elliptic Curve Cryptography (ECDSA, Ed25519)",
                        "Diffie-Hellman ephemeral key exchange (ECDHE) for perfect forward secrecy"
                    ]
                ),
                (
                    "Cryptographic Hashing, Salted Storage & Digital Signatures",
                    "Protect data integrity and store authentication secrets securely using slow cryptographic KDFs.",
                    [
                        "Collision-resistant cryptographic hash functions: SHA-256 and SHA-3",
                        "Password hashing with work factors: bcrypt, Argon2id, and PBKDF2 with unique salts",
                        "Digital signatures: verifying message authenticity and non-repudiation"
                    ]
                ),
                (
                    "Public Key Infrastructure (PKI) & TLS 1.3 Handshake",
                    "Understand how digital certificates establish trust across public Internet communication channels.",
                    [
                        "X.509 digital certificate structure: Subject, Issuer, SAN, and Public Key",
                        "Certificate Authorities (CAs), root trust stores, and certificate revocation (CRL / OCSP)",
                        "The TLS 1.3 handshake: 1-RTT connection setup, cipher suite negotiation, and session resumption"
                    ]
                )
            ],
            "quiz": [
                {
                    "id": 1,
                    "question": "Why should passwords never be stored using fast cryptographic hashes like SHA-256 or MD5, even when salted?",
                    "options": [
                        "Modern GPUs can compute billions of SHA-256 hashes per second, making offline brute-force and dictionary attacks trivially fast",
                        "SHA-256 hashes automatically decrypt after 24 hours",
                        "SHA-256 cannot process passwords longer than 8 characters",
                        "Fast hashes are strictly prohibited by web browser engines"
                    ],
                    "correct_index": 0
                },
                {
                    "id": 2,
                    "question": "In a TLS connection, what does 'Perfect Forward Secrecy' (PFS) guarantee?",
                    "options": [
                        "Compromise of the server's long-term private key in the future will not compromise past recorded session communications",
                        "The server will never experience hardware crashes or downtime",
                        "All client devices are guaranteed to be free of malware",
                        "Passwords are never transmitted over the network in any format"
                    ],
                    "correct_index": 0
                }
            ]
        },
        {
            "day_number": 5,
            "title": "Defensive Security Operations & SIEM Monitoring",
            "subtopics": [
                (
                    "Security Operations Center (SOC) Architecture & Triage Tiers",
                    "Understand SOC operating workflows, tier structures, and alert triage lifecycles.",
                    [
                        "Tier 1 (Triage & Validation), Tier 2 (Investigation), Tier 3 (Threat Hunting & Incident Response)",
                        "Mean Time to Detect (MTTD) and Mean Time to Remediate (MTTR) performance metrics",
                        "Distinguishing true positives, false positives, benign true positives, and false negatives"
                    ]
                ),
                (
                    "SIEM Log Aggregation, Ingestion & Normalization",
                    "Collect and correlate disparate log sources across firewalls, authentication servers, and endpoints.",
                    [
                        "Log sources: Windows Event Logs (Sysmon), Linux auth.log, cloud audit trails (CloudTrail)",
                        "Ingestion pipelines with Elastic SIEM, Splunk, or Wazuh using Common Information Model (CIM)",
                        "Parsing unstructured logs into structured timestamps, source IPs, and action verbs"
                    ]
                ),
                (
                    "Correlation Rules, Anomaly Detection & IOC Hunting",
                    "Write automated detection rules to catch active brute-force, lateral movement, and data staging.",
                    [
                        "Writing Sigma and Splunk SPL / Elasticsearch KQL detection rules",
                        "Detecting suspicious behaviors: impossible travel, privilege escalation, and lateral SSH leaps",
                        "Indicators of Compromise (IOCs) vs Indicators of Attack (IOAs) ingestion via threat intel feeds"
                    ]
                )
            ],
            "quiz": [
                {
                    "id": 1,
                    "question": "In a Security Operations Center (SOC), what does 'Sysmon' provide when installed on Windows endpoints?",
                    "options": [
                        "Advanced system monitoring logging detailed process creations, network connections, and file modification events",
                        "An automated word processor for writing security reports",
                        "A hardware firewall replacement for local area networks",
                        "A web browser extension that blocks phishing websites"
                    ],
                    "correct_index": 0
                },
                {
                    "id": 2,
                    "question": "What is an 'Impossible Travel' alert in cloud identity security?",
                    "options": [
                        "An alert triggered when a single user account logs in from two geographically distant locations within a window of time too short to travel between them",
                        "An alert notifying administrators that a flight ticket was cancelled",
                        "A warning that server latency between continents exceeded 1000ms",
                        "An alert that an employee booked personal travel on a company card"
                    ],
                    "correct_index": 0
                }
            ]
        },
        {
            "day_number": 6,
            "title": "Vulnerability Assessment & Ethical Penetration Testing",
            "subtopics": [
                (
                    "Vulnerability Scanning & Asset Assessment",
                    "Identify unpatched vulnerabilities, misconfigurations, and outdated libraries across infrastructure.",
                    [
                        "Automated vulnerability scanners (Nessus, OpenVAS, Trivy) and credentialed scans",
                        "Common Vulnerabilities and Exposures (CVE) database and CVSS v3.1 scoring metrics",
                        "Prioritizing vulnerability remediation based on active exploit availability (CISA KEV)"
                    ]
                ),
                (
                    "Network Reconnaissance & Port Enumeration with Nmap",
                    "Perform stealthy network mapping, service detection, and script scanning with Nmap.",
                    [
                        "TCP SYN scan (-sS), UDP scan (-sU), and service version detection (-sV)",
                        "Nmap Scripting Engine (NSE) for automated vulnerability probing (e.g. --script vuln)",
                        "Evading basic rate limits and identifying firewall filtering behaviors"
                    ]
                ),
                (
                    "Ethical Penetration Testing Methodologies & Scopes",
                    "Execute authorized offensive testing within legal Rules of Engagement and code of ethics.",
                    [
                        "PTES (Penetration Testing Execution Standard) phases: Pre-engagement, Intelligence Gathering, Exploitation, Reporting",
                        "Black-box, White-box, and Gray-box testing methodologies",
                        "Writing executive penetration testing reports with actionable remediation advice"
                    ]
                )
            ],
            "quiz": [
                {
                    "id": 1,
                    "question": "In CVSS (Common Vulnerability Scoring System) v3.1, what range of scores classifies a vulnerability as 'Critical'?",
                    "options": [
                        "9.0 to 10.0",
                        "7.0 to 8.9",
                        "4.0 to 6.9",
                        "0.1 to 3.9"
                    ],
                    "correct_index": 0
                },
                {
                    "id": 2,
                    "question": "What is the primary difference between a Black-Box and White-Box penetration test?",
                    "options": [
                        "In Black-Box testing, the tester has zero prior knowledge or source code access; in White-Box testing, full architectural knowledge and source code are provided",
                        "Black-Box tests are executed at night; White-Box tests are executed during the day",
                        "Black-Box tests are illegal; White-Box tests are authorized",
                        "Black-Box tests only target hardware routers; White-Box tests only target software code"
                    ],
                    "correct_index": 0
                }
            ]
        },
        {
            "day_number": 7,
            "title": "Incident Response, Digital Forensics & Compliance",
            "subtopics": [
                (
                    "Incident Response Lifecycles (NIST SP 800-61 & SANS PICERL)",
                    "Orchestrate systematic containment, eradication, and recovery from active cyber breaches.",
                    [
                        "The 6 phases: Preparation, Identification, Containment, Eradication, Recovery, Lessons Learned",
                        "Short-term vs long-term containment strategies (network isolation vs live monitoring)",
                        "Conducting blameless Post-Incident Reviews (PIR) and updating defense playbooks"
                    ]
                ),
                (
                    "Digital Forensics, Memory Analysis & Chain of Custody",
                    "Preserve volatile forensic evidence and reconstruct adversary actions across disk and RAM.",
                    [
                        "Order of Volatility: CPU registers, RAM, network state, disk storage, optical media",
                        "Live memory acquisition (LiME / FTK Imager) and memory analysis with Volatility framework",
                        "Maintaining strict Chain of Custody documentation for legal admissibility"
                    ]
                ),
                (
                    "Enterprise Compliance & Governance (ISO 27001 / SOC 2 / DPDP)",
                    "Align security architectures with international regulatory compliance and data protection mandates.",
                    [
                        "ISO/IEC 27001 Information Security Management System (ISMS) controls",
                        "SOC 2 Trust Services Criteria: Security, Availability, Processing Integrity, Confidentiality, Privacy",
                        "Data protection compliance: Indian DPDP Act 2023, GDPR, and breach notification windows"
                    ]
                )
            ],
            "quiz": [
                {
                    "id": 1,
                    "question": "According to the Order of Volatility in digital forensics, which type of evidence must be captured FIRST before powering down a machine?",
                    "options": [
                        "Volatile RAM / System Memory",
                        "Solid State Drive (SSD) partitions",
                        "Archived backup tapes",
                        "Printed system log sheets"
                    ],
                    "correct_index": 0
                },
                {
                    "id": 2,
                    "question": "In the NIST Incident Response lifecycle, what occurs during the 'Eradication' phase?",
                    "options": [
                        "Remnants of the attack (malware, rootkits, compromised accounts, backdoors) are systematically removed from the environment",
                        "The organization issues a press release acknowledging the breach",
                        "The organization purchases new server hardware",
                        "All employee email accounts are permanently deleted"
                    ],
                    "correct_index": 0
                }
            ]
        }
    ]
}


DIGITAL_MARKETING_COURSE = {
    "domain": "Digital Marketing",
    "title": "Growth Engineering, Performance Marketing, SEO & Funnel Analytics",
    "slug": "digital-marketing",
    "level": "Beginner",
    "estimated_hours": 14,
    "banner_gradient": "linear-gradient(135deg, #78350f 0%, #b45309 50%, #d97706 100%)",
    "chapters": [
        {
            "day_number": 1,
            "title": "Marketing Foundations, Customer Acquisition Funnels & Value Propositions",
            "subtopics": [
                (
                    "The Modern Digital Marketing Ecosystem & Omnichannel Strategy",
                    "Understand how paid, earned, shared, and owned media channels integrate into full-funnel engines.",
                    [
                        "PESO model: Paid, Earned, Shared, and Owned media channel distribution",
                        "B2B vs B2C marketing dynamics, buyer cycles, and purchase decision friction",
                        "Omnichannel customer experiences vs siloed multi-channel campaigns"
                    ]
                ),
                (
                    "Customer Acquisition Funnels & Buyer Journey Stages",
                    "Architect full-funnel marketing architectures from top-of-funnel awareness to customer advocacy.",
                    [
                        "AIDA framework: Awareness, Interest, Desire, Action",
                        "TOFU (educational content), MOFU (comparison guides/case studies), and BOFU (demos/trials)",
                        "Identifying and diagnosing funnel drop-off bottlenecks"
                    ]
                ),
                (
                    "Value Propositions, Positioning & Ideal Customer Profiles (ICPs)",
                    "Craft razor-sharp market positioning and define target persona archetypes that drive conversion.",
                    [
                        "Value Proposition Canvas: Customer Jobs, Pains, Gains vs Pain Relievers & Gain Creators",
                        "Developing Ideal Customer Profiles (ICPs) and quantitative buyer personas",
                        "Competitive differentiation and the 'Only-ness' positioning statement"
                    ]
                )
            ],
            "quiz": [
                {
                    "id": 1,
                    "question": "In the PESO marketing model, what category does a company's own official technical blog or website belong to?",
                    "options": [
                        "Owned Media",
                        "Paid Media",
                        "Earned Media",
                        "Shared Media"
                    ],
                    "correct_index": 0
                },
                {
                    "id": 2,
                    "question": "Which stage of the customer acquisition funnel focuses on prospects who understand their problem and are comparing potential solutions?",
                    "options": [
                        "Middle of the Funnel (MOFU)",
                        "Top of the Funnel (TOFU)",
                        "Bottom of the Funnel (BOFU)",
                        "Advocacy / Referral stage"
                    ],
                    "correct_index": 0
                }
            ]
        },
        {
            "day_number": 2,
            "title": "Search Engine Optimization (SEO): Technical Audits, On-Page & Schema Markup",
            "subtopics": [
                (
                    "Search Engine Crawler Mechanics & Core Web Vitals",
                    "Understand how Googlebot crawls, renders, and indexes web content, and optimize page experience signals.",
                    [
                        "The crawl budget, Googlebot rendering pipeline, and indexation controls (robots.txt, sitemaps)",
                        "Core Web Vitals: LCP (Largest Contentful Paint), INP (Interaction to Next Paint), CLS (Cumulative Layout Shift)",
                        "Server-side rendering (SSR) vs static site generation (SSG) impact on search visibility"
                    ]
                ),
                (
                    "On-Page SEO, Keyword Intent & Semantic Content Optimization",
                    "Conduct keyword research, analyze search intent, and optimize on-page content structures.",
                    [
                        "Search intent categorization: Informational, Navigational, Commercial, and Transactional",
                        "Title tags, meta descriptions, H1-H3 header hierarchies, and internal linking architectures",
                        "Entity-based SEO and semantic keyword clustering (NLP / Google Knowledge Graph)"
                    ]
                ),
                (
                    "Structured Data, Schema.org & Rich Search Snippets",
                    "Implement JSON-LD structured data to capture rich search results, FAQ accordions, and star ratings.",
                    [
                        "Schema.org vocabularies: Course, Article, FAQPage, BreadcrumbList, and Organization",
                        "Embedding valid JSON-LD scripts in HTML headers for rich result eligibility",
                        "Testing and debugging with Google Rich Results Test and Search Console inspection tools"
                    ]
                )
            ],
            "quiz": [
                {
                    "id": 1,
                    "question": "In Google Core Web Vitals, what does LCP (Largest Contentful Paint) measure?",
                    "options": [
                        "The time it takes for the largest visual content element (e.g. hero image or heading) to render in the viewport",
                        "The total number of CSS files loaded on the webpage",
                        "The physical distance between the web server and the user",
                        "The time it takes for the user to type a comment"
                    ],
                    "correct_index": 0
                },
                {
                    "id": 2,
                    "question": "What is the recommended format by Google for implementing Schema.org structured data on web pages?",
                    "options": [
                        "JSON-LD embedded within a <script type='application/ld+json'> tag",
                        "Microdata attributes scattered across HTML tags",
                        "Writing XML comments in the footer",
                        "Uploading an unformatted CSV spreadsheet to Google Drive"
                    ],
                    "correct_index": 0
                }
            ]
        },
        {
            "day_number": 3,
            "title": "High-Converting Content Strategy, Copywriting & Email Marketing Automation",
            "subtopics": [
                (
                    "Content Marketing Strategy & Topic Clusters",
                    "Build organic search authority and brand trust through comprehensive pillar pages and topic cluster models.",
                    [
                        "Pillar-and-cluster content architecture: high-authority pillar guides linking to specific cluster subtopics",
                        "Content calendars, cadence planning, and evergreen asset curation",
                        "Repurposing long-form content into bite-sized social carousels and newsletter snippets"
                    ]
                ),
                (
                    "Direct Response Copywriting & Behavioral Psychology",
                    "Craft high-converting headlines, landing pages, and calls-to-action utilizing psychological persuasion triggers.",
                    [
                        "Proven copywriting frameworks: PAS (Problem-Agitate-Solve) and BAB (Before-After-Bridge)",
                        "Microcopy, button CTA psychology, and reducing perceived cognitive friction",
                        "Social proof, authority badges, and risk reversal guarantees"
                    ]
                ),
                (
                    "Lifecycle Email Marketing & Automation Drip Sequences",
                    "Design high-performing email sequences for onboarding, engagement, retention, and churn prevention.",
                    [
                        "Behavioral triggers: welcome drips, abandoned action sequences, and re-engagement campaigns",
                        "List segmentation based on domain, user lifecycle stage, and email engagement activity",
                        "Email deliverability hygiene: SPF, DKIM, DMARC, sender reputation, and spam score audits"
                    ]
                )
            ],
            "quiz": [
                {
                    "id": 1,
                    "question": "In the PAS copywriting framework, what does 'A' stand for?",
                    "options": [
                        "Agitate",
                        "Action",
                        "Audience",
                        "Authority"
                    ],
                    "correct_index": 0
                },
                {
                    "id": 2,
                    "question": "Which trio of DNS authentication records is essential to ensure legitimate email delivery and prevent spoofing in Gmail and Yahoo inboxes?",
                    "options": [
                        "SPF, DKIM, and DMARC",
                        "CNAME, A, and AAAA",
                        "TXT, NS, and SOA",
                        "MX, PTR, and BIND"
                    ],
                    "correct_index": 0
                }
            ]
        },
        {
            "day_number": 4,
            "title": "Paid Advertising (PPC): Google Search, Meta Ads & Audience Segmentation",
            "subtopics": [
                (
                    "Google Ads & Paid Search Auction Economics",
                    "Master Google Search Ads: keyword match types, auction mechanics, Quality Scores, and bidding strategies.",
                    [
                        "Ad Rank formula: Max CPC Bid multiplied by Quality Score (Ad relevance, CTR, Landing page experience)",
                        "Keyword match types: Exact match, Phrase match, and Broad match modifiers",
                        "Smart Bidding algorithms: Target CPA, Target ROAS, and Maximize Conversions"
                    ]
                ),
                (
                    "Meta Ads Architecture & The Conversion API (CAPI)",
                    "Construct high-ROI paid social campaigns across Facebook and Instagram with advanced targeting.",
                    [
                        "Campaign hierarchy: Campaign objective, Ad Set targeting, and Ad Creative formats",
                        "Custom Audiences, Lookalike Audiences (1-3%), and broad demographic targeting",
                        "Meta Conversions API (CAPI) server-side event tracking to counter iOS ATT privacy loss"
                    ]
                ),
                (
                    "Creative Strategy, Ad Fatigue & Multivariate A/B Testing",
                    "Develop dynamic creative variations and execute structured testing to beat creative fatigue.",
                    [
                        "Hook-Hold-Payoff video creative structures for short-form video ads (Reels/TikTok)",
                        "Analyzing Thumbstop Rate (3-sec view / Impressions) and Hold Rate (15-sec view / 3-sec view)",
                        "Statistical significance in A/B split testing (p-value < 0.05) before scaling ad budgets"
                    ]
                )
            ],
            "quiz": [
                {
                    "id": 1,
                    "question": "In Google Search Ads auction economics, how can an advertiser with a lower CPC bid rank higher than a competitor with a higher bid?",
                    "options": [
                        "By achieving a substantially higher Quality Score through relevant ad copy, high CTR, and superior landing page experience",
                        "By running ads only between midnight and 6 AM",
                        "By paying Google an annual membership fee",
                        "By using only single-word keywords"
                    ],
                    "correct_index": 0
                },
                {
                    "id": 2,
                    "question": "Why is Meta's Conversions API (CAPI) critical for performance marketers following Apple's iOS 14.5 App Tracking Transparency (ATT) update?",
                    "options": [
                        "CAPI sends conversion events directly from the server to Meta, bypassing client-side browser ad-blockers and cookie restrictions",
                        "CAPI automatically writes all ad copy using AI models",
                        "CAPI guarantees a 10x Return on Ad Spend (ROAS)",
                        "CAPI eliminates the need for ad creatives"
                    ],
                    "correct_index": 0
                }
            ]
        },
        {
            "day_number": 5,
            "title": "Web Analytics, Google Analytics 4 (GA4), Event Tracking & Conversion Rate Optimization (CRO)",
            "subtopics": [
                (
                    "Google Analytics 4 (GA4) Architecture & Event-Driven Models",
                    "Understand GA4's flexible event-based data model replacing legacy session-based Universal Analytics.",
                    [
                        "Event-driven architecture: automatically collected, enhanced measurement, and custom events",
                        "Custom dimensions, metrics, and user properties configuration in GA4",
                        "User acquisition vs traffic acquisition reports and engagement rate metrics"
                    ]
                ),
                (
                    "Google Tag Manager (GTM) & DataLayer Instrumentation",
                    "Deploy custom tracking tags, triggers, and variables without requiring continuous code changes.",
                    [
                        "GTM container architecture: Tags (what runs), Triggers (when it runs), Variables (what values)",
                        "Instrumenting custom DataLayer push events for checkout steps and form submissions",
                        "Preview mode debugging and validating cross-domain measurement"
                    ]
                ),
                (
                    "Conversion Rate Optimization (CRO) & Heatmap Analysis",
                    "Identify friction points on high-value landing pages and optimize conversion funnels.",
                    [
                        "Heatmap, scroll map, and session recording analysis with Microsoft Clarity or Hotjar",
                        "Form analytics: field abandonment rates, error friction, and completion time audits",
                        "Iterative conversion experiments: hypothesis formulation, micro-copy tweaks, and social proof placement"
                    ]
                )
            ],
            "quiz": [
                {
                    "id": 1,
                    "question": "What is the foundational data model of Google Analytics 4 (GA4) compared to legacy Universal Analytics?",
                    "options": [
                        "An Event-based data model where all user interactions (page views, clicks, scrolls, purchases) are tracked as events with parameters",
                        "A Session-based model that groups all hits into rigid 30-minute buckets",
                        "A pure server-log parsing model that does not run JavaScript",
                        "A database query model that only tracks SQL transactions"
                    ],
                    "correct_index": 0
                },
                {
                    "id": 2,
                    "question": "In Google Tag Manager (GTM), what is the 'dataLayer'?",
                    "options": [
                        "A JavaScript array on the page that temporarily holds information to be passed to GTM tags and third-party analytics tools",
                        "A permanent PostgreSQL database hosted on Google Cloud",
                        "A stylesheet layer that controls the visual appearance of Google Ads",
                        "An encryption algorithm that hides website code from competitors"
                    ],
                    "correct_index": 0
                }
            ]
        },
        {
            "day_number": 6,
            "title": "Social Media Growth Engineering, Influencer Partnerships & Viral Loops",
            "subtopics": [
                (
                    "Organic Algorithm Dynamics: LinkedIn, X, Instagram & YouTube",
                    "Understand ranking signals, engagement velocity, and retention metrics governing social distribution.",
                    [
                        "Platform algorithm mechanics: engagement velocity (first 60 minutes), dwell time, and shares",
                        "B2B organic growth on LinkedIn: text-and-image carousels, personal branding, and thought leadership",
                        "Short-form video algorithms (Reels/Shorts): watch time completion rates and loop replays"
                    ]
                ),
                (
                    "Influencer Marketing & Creator Partnerships",
                    "Identify, vet, negotiate, and execute creator collaborations that drive authentic conversion.",
                    [
                        "Evaluating creator authenticity: engagement rate (ER) benchmarks, audience quality, and fake follower audits",
                        "Micro-influencers (10k-50k followers) vs macro-influencers: niche trust and cost efficiency",
                        "Contractual terms, usage rights, whitelisting (creator licensing), and UTM tracking links"
                    ]
                ),
                (
                    "Viral Loops, Referral Programs & Community-Led Growth",
                    "Engineer self-sustaining referral loops where each new customer invites subsequent users.",
                    [
                        "The Viral Coefficient (K-factor): formula K = i * c (invites per user * conversion rate)",
                        "Two-sided referral incentives (e.g. 'Give $10, Get $10' / Coin rewards)",
                        "Community-led growth: hosting developer hackathons, Discord/Slack communities, and brand ambassadors"
                    ]
                )
            ],
            "quiz": [
                {
                    "id": 1,
                    "question": "In viral growth engineering, what does a K-factor (viral coefficient) greater than 1.0 (K > 1) signify?",
                    "options": [
                        "The product is experiencing viral exponential growth, as each new user brings in more than one additional user on average",
                        "The marketing budget is being depleted at an unsustainable rate",
                        "The website server is failing due to high network latency",
                        "The product has lost 50% of its customer base"
                    ],
                    "correct_index": 0
                },
                {
                    "id": 2,
                    "question": "Why do micro-influencers (10,000 to 50,000 followers) frequently yield higher campaign ROI than celebrity influencers for niche products?",
                    "options": [
                        "They typically possess higher audience engagement rates, deeper domain trust, and cost significantly less per acquisition",
                        "They are the only creators permitted to run paid advertisements by law",
                        "They automatically guarantee 100,000 website visits per post",
                        "They own the social media platform servers"
                    ],
                    "correct_index": 0
                }
            ]
        },
        {
            "day_number": 7,
            "title": "Growth Marketing Metrics (LTV, CAC, ROAS), Multi-Touch Attribution & Marketing Capstone",
            "subtopics": [
                (
                    "Core Financial Unit Economics: CAC, LTV & Payback Period",
                    "Calculate fundamental growth metrics to ensure profitable and sustainable customer acquisition.",
                    [
                        "Customer Acquisition Cost (CAC): total sales & marketing spend divided by new customers acquired",
                        "Customer Lifetime Value (LTV): average order value * purchase frequency * customer lifespan * gross margin",
                        "The Golden Ratio: LTV:CAC >= 3:1 and CAC Payback Period under 12 months"
                    ]
                ),
                (
                    "Multi-Touch Attribution Modeling & Marketing Mix Modeling",
                    "Attribute revenue fairly across multiple marketing touchpoints rather than relying on flawed single-touch models.",
                    [
                        "Attribution models: First-touch (discovery), Last-touch (closing), Linear, and Data-Driven",
                        "The limitations of last-click attribution in multi-channel buyer journeys",
                        "Marketing Mix Modeling (MMM) and media incrementality testing to measure true channel lift"
                    ]
                ),
                (
                    "Integrated Growth Marketing Strategy & Executive Dashboard",
                    "Synthesize all acquisition, engagement, and retention strategies into an executive growth roadmap.",
                    [
                        "Constructing a North Star Metric (NSM) and supporting operational KPIs",
                        "Building executive marketing reporting dashboards in Looker Studio or Power BI",
                        "Presenting marketing return on investment (ROAS) and budget allocation requests to executive leadership"
                    ]
                )
            ],
            "quiz": [
                {
                    "id": 1,
                    "question": "What is the widely accepted benchmark for the LTV:CAC ratio in a healthy, sustainable software or subscription business?",
                    "options": [
                        "3:1 or higher (Customer Lifetime Value is at least 3 times the Acquisition Cost)",
                        "1:1 (Revenue equals acquisition cost exactly)",
                        "1:3 (Acquisition cost is 3 times higher than revenue)",
                        "0:1 (Customers are acquired without any revenue)"
                    ],
                    "correct_index": 0
                },
                {
                    "id": 2,
                    "question": "What is the primary flaw of 'Last-Click Attribution' when evaluating multi-channel marketing campaigns?",
                    "options": [
                        "It gives 100% of the conversion credit to the final touchpoint (often branded search or direct), completely ignoring the top-of-funnel channels that introduced the customer",
                        "It requires the marketing team to calculate taxes manually",
                        "It does not work with Google Analytics 4",
                        "It only measures customers who visit a physical retail store"
                    ],
                    "correct_index": 0
                }
            ]
        }
    ]
}

# Master list of the 5 newly expanded 7-day courses
NEW_7DAY_DOMAIN_COURSES = [
    UI_UX_DESIGN_COURSE,
    DEVOPS_CLOUD_COURSE,
    MOBILE_APP_DEVELOPMENT_COURSE,
    CYBERSECURITY_COURSE,
    DIGITAL_MARKETING_COURSE,
]


# ================================================================================
# 4 Existing Platform Courses (Days 1–7 Synchronized from Production EC2)
# ================================================================================

DATA_ANALYST_COURSE = {
    "domain": "Data Analyst",
    "title": "Data Analytics Accelerated: Practical EDA, SQL & Business Intelligence",
    "slug": "data-analytics-accelerated",
    "level": "Beginner to Intermediate",
    "estimated_hours": 14,
    "banner_gradient": "linear-gradient(135deg, #0284c7, #2563eb)",
    "chapters": [
        {
            "day_number": 1,
            "title": "Foundations of Exploratory Data Analysis & Analytical Thinking",
            "subtopics": [
                (
                    "Problem Framing & The Business Intelligence Lifecycle",
                    "Learn how raw transactional events transform into decision-grade intelligence. We examine the full BI lifecycle: data capture, ingestion pipelines, dimensional staging, and analytics consumption. Master the MECE (Mutually Exclusive, Collectively Exhaustive) framework to translate ambiguous business complaints (e.g. 'churn is accelerating') into structured, testable analytical questions.",
                    ["Differentiate between passive descriptive reporting and root-cause diagnostic analytics.", "Structure complex business investigations using the MECE hypothesis framework.", "Map the journey of raw tabular data from transactional systems (OLTP) to analytical datamarts (OLAP)."]
                ),
                (
                    "Data Types, Schemas & Quality Audit Metrics",
                    "Before computing any KPI, a professional analyst performs a rigorous data audit. Understand the mathematical implications of nominal, ordinal, interval, and ratio scales. Learn systematic techniques to audit missingness (MCAR vs MAR vs MNAR), detect silent schema coercions, resolve timezone offsets, and handle duplicate entity records.",
                    ["Perform pre-analysis data health audits covering completeness, validity, uniqueness, and consistency.", "Distinguish between structural nulls (e.g. missing discount on non-promotional item) and data capture failures.", "Identify and remedy common timezone and date-boundary distortions in daily metric rollups."]
                ),
                (
                    "Summary Statistics, Percentiles & Skewness",
                    "Explore the reality of skewed real-world business data where naive averages mislead stakeholders. Master non-parametric summary statistics: medians, Interquartile Ranges (IQR), and percentile distributions (P50, P90, P99). Learn how to detect outliers, quantify metric variance, and communicate risk and distribution shape to non-technical stakeholders.",
                    ["Recognize heavily skewed metrics (order values, customer spend, SLA response times) where median and IQR are mandatory.", "Calculate and interpret IQR-based statistical fences to identify genuine anomalies vs extreme normal behavior.", "Explain the dangers of optimizing business operations against a simple arithmetic mean."]
                ),
            ],
            "quiz": [
                {"id": 1, "question": "What is the main topic covered in Day 1?", "options": ["Foundations of Exploratory Data Analysis & Analytical Thinking", "General Overview", "Advanced Topics", "None of these"], "correct_index": 0},
                {"id": 2, "question": "What is the primary benefit of Python automation?", "options": ["Saves time & reduces human error", "Slows down code execution", "Requires extra hardware", "Increases manual data entry"], "correct_index": 0},
            ]
        },
        {
            "day_number": 2,
            "title": "Advanced Tabular Modeling & Excel for Analysts",
            "subtopics": [
                (
                    "Dynamic Multi-Condition Lookups (XLOOKUP & Index-Match)",
                    "Transition beyond legacy, fragile VLOOKUPs to resilient lookup architectures. Master INDEX-MATCH for two-way matrix coordinate lookups across arbitrary row and column headers. Implement modern XLOOKUP with search modes, wildcard matching, default fallback values, and approximate match lookup tables for tiered pricing and commission slabs.",
                    ["Build resilient, bidirectional table lookups that do not break when columns are inserted or reordered.", "Implement exact-match multi-criteria lookups using Boolean arrays inside XLOOKUP.", "Configure approximate lookups for bracketed calculations (tax tiers, performance bonuses, shipping rate cards)."]
                ),
                (
                    "Dimensional Pivot Tables, Slicers & Calculated Fields",
                    "Transform large transaction logs into responsive analytical matrices. Learn how to group continuous date sequences into custom fiscal periods, build calculated fields without modifying source records, configure custom 'Show Values As' calculations (% of row total, difference from previous period), and connect multiple pivots to unified visual slicers.",
                    ["Summarize multidimensional datasets without writing redundant helper columns.", "Leverage built-in relative calculations to compute Month-over-Month (MoM) deltas directly in Pivot Tables.", "Design linked interactive dashboard slices with synchronized timeline and category controls."]
                ),
                (
                    "Automating Tabular Pipelines with Power Query",
                    "Automate routine data ingestion, unpivoting, and transformation using Power Query's M-engine. Learn to unpivot cross-tabulated reports into clean, normalized tabular formats (tidy data). Standardize casing, parse embedded text structures, merge multiple CSV files dynamically, and build zero-maintenance refreshable workflows.",
                    ["Convert wide matrix reports into normalized, query-ready 3-column schemas (Date, Dimension, Value).", "Build automated data ingestion queries that refresh automatically when source files update.", "Standardize messy string anomalies and split compound product codes using Power Query transformations."]
                ),
            ],
            "quiz": [
                {"id": 1, "question": "What is the main topic covered in Day 2?", "options": ["Advanced Tabular Modeling & Excel for Analysts", "General Overview", "Advanced Topics", "None of these"], "correct_index": 0},
                {"id": 2, "question": "What is the primary benefit of Python automation?", "options": ["Saves time & reduces human error", "Slows down code execution", "Requires extra hardware", "Increases manual data entry"], "correct_index": 0},
            ]
        },
        {
            "day_number": 3,
            "title": "Relational Data Extraction & SQL Foundations",
            "subtopics": [
                (
                    "Logical Query Processing Order & Selective Filtering",
                    "Master the logical lifecycle of SQL execution. Understand why queries execute in the order: FROM -> WHERE -> GROUP BY -> HAVING -> SELECT -> ORDER BY -> LIMIT, rather than the lexical order in which they are written. Master predicate pushdown, SARGable filter expressions (avoiding functions in WHERE clauses), and distinguishing WHERE from HAVING.",
                    ["Understand SQL engine execution sequence to troubleshoot aliasing and scoping errors.", "Apply pre-aggregation filtering with WHERE to reduce working dataset size before grouping.", "Write SARGable queries that utilize B-tree indexes rather than forcing full table scans."]
                ),
                (
                    "Relational Joins, Cardinality & Cartesian Traps",
                    "Join disparate tables while preserving analytical truth. Dive deep into INNER, LEFT, RIGHT, and FULL OUTER joins. Understand join cardinality (1:1, 1:N, N:M) and learn how unintentional many-to-many joins cause catastrophic cartesian explosions that silently double-count financial totals.",
                    ["Select the appropriate join type based on whether non-matching parent records must be preserved.", "Audit record counts before and after joins to verify that cardinality matches domain expectations.", "Join transactional fact tables to dimensional entity tables without creating metric inflation."]
                ),
                (
                    "Multi-Metric Conditional Aggregations with CASE WHEN",
                    "Transform vertical records into horizontal summary dashboards in a single SQL pass. Master conditional aggregation using SUM(CASE WHEN ... THEN 1 ELSE 0 END) and COUNT(DISTINCT CASE WHEN ...). Calculate funnel conversion rates, status breakdowns, and cohort metrics without writing multiple separate queries.",
                    ["Pivot status categories into dedicated KPI columns in a single table scan.", "Compute conversion ratios and retention fractions directly within SQL SELECT statements.", "Safely manage division-by-zero errors using NULLIF within aggregate calculations."]
                ),
            ],
            "quiz": [
                {"id": 1, "question": "What is the main topic covered in Day 3?", "options": ["Relational Data Extraction & SQL Foundations", "General Overview", "Advanced Topics", "None of these"], "correct_index": 0},
                {"id": 2, "question": "What is the primary benefit of Python automation?", "options": ["Saves time & reduces human error", "Slows down code execution", "Requires extra hardware", "Increases manual data entry"], "correct_index": 0},
            ]
        },
        {
            "day_number": 4,
            "title": "Analytical SQL: Window Functions & Common Table Expressions",
            "subtopics": [
                (
                    "Modular Query Design with Common Table Expressions (CTEs)",
                    "Deconstruct complex business logic into readable, maintainable, and modular CTE pipelines. Compare the execution characteristics of CTEs (`WITH` clauses) vs subqueries and temporary staging tables. Learn how to structure analytical scripts into clean semantic layers: data extraction, cleaning, metric aggregation, and final presentation.",
                    ["Replace unreadable nested subqueries with linear, self-documenting CTE stages.", "Improve collaborative code maintainability and peer review readability across analytics teams.", "Structure complex multi-pass transformations into modular analytical pipelines."]
                ),
                (
                    "Ranking & Value Window Functions (ROW_NUMBER, DENSE_RANK, LAG/LEAD)",
                    "Perform sophisticated intra-group analytical calculations without collapsing row cardinality. Master the OVER clause with PARTITION BY and ORDER BY. Use ROW_NUMBER() for precise deduplication, DENSE_RANK() for top-N ranking, and LAG()/LEAD() to compute Period-over-Period growth and user lifecycle intervals.",
                    ["Isolate top N records per dimensional category using `ROW_NUMBER() OVER(PARTITION BY ... ORDER BY ...)`.", "Differentiate the behavior of RANK (gaps on ties) and DENSE_RANK (continuous sequence).", "Calculate Month-over-Month (MoM) revenue growth using `LAG(revenue, 1)`."]
                ),
                (
                    "Rolling Aggregates & Dynamic Window Framing",
                    "Smooth volatile business metrics and track trajectory trends using rolling window frames. Master window framing specifications (`ROWS BETWEEN 6 PRECEDING AND CURRENT ROW`). Build running year-to-date (YTD) cumulative sums, 7-day moving averages for operational pacing, and 30-day churn baselines.",
                    ["Calculate running totals and cumulative metric trajectories without self-joins.", "Build rolling moving averages to distinguish true trend signals from weekday/weekend noise.", "Understand the critical difference between ROWS (physical rows) and RANGE (logical value offsets)."]
                ),
            ],
            "quiz": [
                {"id": 1, "question": "What is the main topic covered in Day 4?", "options": ["Analytical SQL: Window Functions & Common Table Expressions", "General Overview", "Advanced Topics", "None of these"], "correct_index": 0},
                {"id": 2, "question": "What is the primary benefit of Python automation?", "options": ["Saves time & reduces human error", "Slows down code execution", "Requires extra hardware", "Increases manual data entry"], "correct_index": 0},
            ]
        },
        {
            "day_number": 5,
            "title": "Python for Data Analysis: Vectorized NumPy & Pandas",
            "subtopics": [
                (
                    "Vectorized Computing & Boolean Indexing with NumPy",
                    "Explore the foundation of modern high-performance data manipulation in Python. Understand how NumPy ndarrays store homogeneous data contiguously in memory. Compare C-speed vectorized operations against slow interpreted Python loops. Master boolean masking, broadcasting rules, and numerical aggregation across multidimensional axes.",
                    ["Eliminate slow `for` loops in Python by replacing them with SIMD-accelerated vectorized operations.", "Filter and transform large numerical arrays instantaneously using boolean masks.", "Understand array broadcasting rules when operating on arrays with differing dimensions."]
                ),
                (
                    "Data Wrangling, Slicing & Method Chaining with Pandas",
                    "Master idiomatic Pandas operations. Understand the internal anatomy of DataFrames and Series. Differentiate between label-based indexing (`.loc`) and positional indexing (`.iloc`). Avoid the notorious `SettingWithCopyWarning` through explicit view vs copy handling. Structure elegant, readable data pipelines using method chaining (`.assign()`, `.pipe()`, `.query()`).",
                    ["Confidently slice, filter, and modify DataFrames using `.loc` and `.iloc` without accidental side-effects.", "Diagnose and eliminate `SettingWithCopyWarning` by using `.copy()` and proper index assignment.", "Write expressive, maintainable data pipelines using fluent method chaining."]
                ),
                (
                    "Multi-Table Joins, GroupBy Aggregations & Reshaping",
                    "Merge heterogeneous data sources and reshape datasets into analytical form. Master `pd.merge()` with join validation (`validate='1:m'`). Leverage `.groupby()` paired with custom `.agg()` dictionaries to compute multiple metrics per dimension simultaneously. Learn how to pivot and melt between wide reporting formats and tidy tables.",
                    ["Perform relational joins in Pandas while enforcing cardinality constraints using the `validate` parameter.", "Compute multi-metric aggregations (mean, median, count, percentiles) across groups in a single call.", "Reshape DataFrames seamlessly using `.melt()` and `.pivot_table()` for visualization readiness."]
                ),
            ],
            "quiz": [
                {"id": 1, "question": "What is the main topic covered in Day 5?", "options": ["Python for Data Analysis: Vectorized NumPy & Pandas", "General Overview", "Advanced Topics", "None of these"], "correct_index": 0},
                {"id": 2, "question": "What is the primary benefit of Python automation?", "options": ["Saves time & reduces human error", "Slows down code execution", "Requires extra hardware", "Increases manual data entry"], "correct_index": 0},
            ]
        },
        {
            "day_number": 6,
            "title": "Exploratory Visualization & Dashboard Architecture",
            "subtopics": [
                (
                    "Visual Encodings & Chart Selection Frameworks",
                    "Explore the science of visual perception and graphical integrity. Learn how human vision processes pre-attentive attributes (position, length, color hue, size). Master the taxonomy of chart selection: scatter plots for correlation, line charts for continuous temporal trend, bar charts for discrete comparison, and heatmaps for matrix density. Avoid deceptive visual anti-patterns.",
                    ["Select visual encodings based on data relationship types rather than aesthetic whim.", "Adhere to baseline rules: why bar charts strictly require zero baselines while line charts can be cropped.", "Minimize cognitive load and non-data ink by applying Edward Tufte's design principles."]
                ),
                (
                    "Actionable Business Dashboard Architecture (Power BI / Tableau)",
                    "Learn how enterprise BI developers build decision-oriented dashboards. Explore the visual hierarchy: Executive KPI cards at the top, trend context in the middle, and dimensional granular breakdowns at the bottom. Master interactive filtering flows, drill-through paths, and designing for executive decision-makers who spend under 30 seconds scanning a screen.",
                    ["Structure layout hierarchy using standard F-pattern viewing conventions.", "Design rich KPI cards combining current values, benchmark targets, and sparkline trajectories.", "Implement synchronized cross-filtering to enable intuitive root-cause exploration."]
                ),
                (
                    "Statistical Plotting with Seaborn & Interactive Plotly",
                    "Bridge exploratory code and stakeholder presentation. Leverage Seaborn to visualize statistical distributions (KDE, boxplots with overlaid strip plots, violin plots) and correlation heatmaps with annotated coefficients. Use Plotly to create web-ready, interactive charts with hover tooltips and dynamic zooming.",
                    ["Build correlation heatmaps with annotated Pearson/Spearman coefficients to identify multicollinearity.", "Combine boxplots with jittered strip plots to display both statistical summaries and true sample density.", "Generate interactive HTML visualization widgets using Plotly for stakeholder distribution."]
                ),
            ],
            "quiz": [
                {"id": 1, "question": "What is the main topic covered in Day 6?", "options": ["Exploratory Visualization & Dashboard Architecture", "General Overview", "Advanced Topics", "None of these"], "correct_index": 0},
                {"id": 2, "question": "What is the primary benefit of Python automation?", "options": ["Saves time & reduces human error", "Slows down code execution", "Requires extra hardware", "Increases manual data entry"], "correct_index": 0},
            ]
        },
        {
            "day_number": 7,
            "title": "End-to-End Analytics Capstone & Executive Communication",
            "subtopics": [
                (
                    "Formulating Analytical Hypotheses & Project Charters",
                    "Transition from individual technical tasks to leading an end-to-end analytical project. Learn how to draft a structured data project charter: problem statement, measurable success criteria, primary and guardrail metrics, and risk assessment. Formulate testable, falsifiable business hypotheses before writing a single line of query code.",
                    ["Establish clear primary North Star metrics and counter-balancing guardrail metrics to prevent unintended business harm.", "Write testable analytical hypotheses with explicitly defined success/failure thresholds.", "Align project scope, stakeholder expectations, and timeline milestones before commencing exploration."]
                ),
                (
                    "End-to-End Analytics Pipeline: Ingestion to RFM Modeling",
                    "Execute a complete customer analytics case study. Ingest raw multi-table e-commerce data, sanitize timestamps and null values, build a Recency, Frequency, Monetary (RFM) segmentation engine in SQL and Python, score customer cohorts into tiers (Champions, At-Risk, Hibernating), and identify specific actionable revenue opportunities.",
                    ["Compute Recency (days since last purchase), Frequency (order count), and Monetary value (total spend) scores.", "Segment customer populations into distinct behavioral tiers to tailor commercial interventions.", "Translate raw cluster metrics into concrete business implications (e.g. churn prevention vs re-activation)."]
                ),
                (
                    "Executive Data Storytelling & The SCR Communication Framework",
                    "Deliver findings that drive executive decisions. Learn the Barbara Minto Pyramid Principle and the Situation-Complication-Resolution (SCR) storytelling framework. Master the one-page executive memo format. Practice leading with recommendations rather than technical methodology, handling executive skepticism, and quantifying financial business impact.",
                    ["Lead communications with the core bottom-line recommendation (Pyramid Principle), not the step-by-step methodology.", "Structure compelling business narratives using Situation, Complication, and Resolution (SCR).", "Quantify financial ROI and operational effort so leadership can make immediate, confident decisions."]
                ),
            ],
            "quiz": [
                {"id": 1, "question": "What is the main topic covered in Day 7?", "options": ["End-to-End Analytics Capstone & Executive Communication", "General Overview", "Advanced Topics", "None of these"], "correct_index": 0},
                {"id": 2, "question": "What is the primary benefit of Python automation?", "options": ["Saves time & reduces human error", "Slows down code execution", "Requires extra hardware", "Increases manual data entry"], "correct_index": 0},
            ]
        },
    ]
}

AI_AGENT_DEVELOPMENT_COURSE = {
    "domain": "AI Agent Development",
    "title": "Applied AI Agents: Production RAG, Tool Calling & Multi-Agent Orchestration",
    "slug": "ai-agent-development",
    "level": "Intermediate to Advanced",
    "estimated_hours": 20,
    "banner_gradient": "linear-gradient(135deg, #8B5CF6, #6D28D9)",
    "chapters": [
        {
            "day_number": 1,
            "title": "Day 1: LLM Architectures, Prompt Engineering & Structured Outputs",
            "subtopics": [
                (
                    "Foundation Models, Tokenomics & Inference Parameters",
                    "Deep dive into autoregressive transformer models (GPT-4, Gemini 1.5/2.0, Claude 3.5, and open-weight models like Qwen/Llama). Understand tokenization algorithms (Byte-Pair Encoding - BPE) and token-to-word ratios. Master LLM inference hyperparameters: Temperature (controlling probability entropy), Top-P (nucleus sampling), Frequency and Presence Penalties. Calculate operational cost and latency based on prompt and completion token counts.",
                    ["Calculate token usage and API operational costs across frontier foundation models.", "Tune temperature and top_p hyperparameters for deterministic extraction vs creative reasoning.", "Manage context window limits and avoid prompt truncation errors."]
                ),
                (
                    "Production Prompt Engineering & In-Context Learning",
                    "Move from ad-hoc prompting to robust prompt engineering. Master structural role formatting (System, User, Assistant). Implement Chain-of-Thought (CoT) reasoning to force models to 'think' step-by-step before answering. Construct Few-Shot exemplars to anchor output formatting and domain nuance. Implement prompt injection defenses: isolating untrusted user text inside XML/Markdown tags and instructing models to ignore embedded instructions.",
                    ["Formulate Chain-of-Thought prompts that dramatically boost complex mathematical and reasoning accuracy.", "Design few-shot demonstration exemplars that eliminate ambiguous formatting.", "Harden system prompts against prompt injection and jailbreak exploits."]
                ),
                (
                    "Structured Outputs & Schema Enforcement with Pydantic",
                    "Eliminate brittle regex parsing and hallucinated syntax. Force LLMs to generate 100% valid, type-safe JSON adhering strictly to JSON Schema definitions using native Structured Outputs (OpenAI, Gemini) and Pydantic models. Validate field types, optionality, string patterns, and value ranges. Build self-healing schema retry wrappers that pass validation error traces back to the model upon parsing failure.",
                    ["Enforce strict JSON schema compliance using Pydantic data models.", "Guarantee type-safe output ingestion directly into application databases and APIs.", "Implement automated error-feedback retry loops for malformed schema payloads."]
                ),
            ],
            "quiz": [
                {"id": 1, "question": "What is the mathematical effect of setting an LLM's 'temperature' parameter to 0.0 during text generation?", "options": ["The model stops generating text completely", "The model behaves deterministically by greedily selecting the token with the highest log-probability at each step", "The model samples uniformly at random across its entire vocabulary", "The context window size is reduced by half"], "correct_index": 1},
                {"id": 2, "question": "Why is Chain-of-Thought (CoT) prompting effective at solving multi-step mathematical or reasoning problems?", "options": ["It compiles the prompt into native C++ code", "It grants the model additional compute and token steps to derive intermediate states before committing to a final answer", "It bypasses the LLM's token rate limiter", "It forces the model to search Google in the background"], "correct_index": 1},
                {"id": 3, "question": "What distinguishes native LLM 'Structured Outputs' from naive prompt instructions like 'Respond in JSON'?", "options": ["Structured Outputs use grammar-constrained sampling at decoding time to mathematically guarantee schema adherence", "Structured Outputs take 10x longer to generate tokens", "Structured Outputs cannot validate string lengths or numbers", "Structured Outputs work only with XML and not JSON"], "correct_index": 0},
                {"id": 4, "question": "What is the primary objective of an indirect prompt injection attack?", "options": ["To overheat the server GPU hardware", "To embed malicious instructions within third-party data (like web pages or emails) that hijack the LLM's execution flow", "To steal SSL certificates directly from the hosting Linux kernel", "To force the model to decrease its context window"], "correct_index": 1},
                {"id": 5, "question": "In tokenomics, approximately how many English words does a typical prompt containing 1,000 tokens represent?", "options": ["100 words", "750 words", "3,000 words", "10,000 words"], "correct_index": 1},
            ]
        },
        {
            "day_number": 2,
            "title": "Day 2: Vector Embeddings, Semantic Search & Vector Database Architecture",
            "subtopics": [
                (
                    "Dense Embeddings & Vector Similarity Mathematics",
                    "Explore the mathematics of vector embeddings. Contrast sparse keyword vectors (TF-IDF, BM25) with dense semantic embeddings (OpenAI text-embedding-3, HuggingFace sentence-transformers). Understand how transformer encoders map textual semantics into high-dimensional geometric spaces (384 to 3072 dimensions). Calculate geometric distance metrics: Cosine Similarity, Dot Product, and Euclidean (L2) distance, and understand when each metric is appropriate.",
                    ["Understand the mathematical principles governing dense vector embeddings.", "Select appropriate distance metrics (Cosine vs L2) based on vector normalization.", "Evaluate embedding models based on benchmark performance (MTEB) and latency."]
                ),
                (
                    "Vector Databases & High-Performance Indexing (FAISS & Chroma)",
                    "Examine the architecture of dedicated vector storage engines: FAISS (Facebook AI Similarity Search), ChromaDB, Qdrant, and pgvector. Understand why exact k-Nearest Neighbors (k-NN) fails at scale. Dive into Approximate Nearest Neighbor (ANN) indexing structures: Inverted File Indexing (IVF) and Hierarchical Navigable Small World (HNSW) graphs. Benchmark trade-offs between search latency, index build time, and recall precision.",
                    ["Build, persist, and query in-memory and disk-backed vector indexes with FAISS and ChromaDB.", "Tune HNSW index parameters (M, efConstruction, efSearch) for optimal search speed and recall.", "Persist and reload serialized vector index artifacts efficiently in production."]
                ),
                (
                    "Document Ingestion, Chunking Strategies & Metadata Tagging",
                    "Build the document ingestion pipeline. Extract raw text from diverse formats: PDFs (using pdfplumber and PyPDF2), Markdown, and HTML. Compare text chunking strategies: naive fixed-character chunking, recursive character chunking based on semantic boundaries (paragraphs, sentences), and document-structure chunking. Configure chunk overlap to preserve context across boundaries and attach rich metadata (source, page number, timestamp) for filtered retrieval.",
                    ["Extract clean, tabular, and textual content from unstructured PDF documents.", "Implement recursive character chunking that preserves semantic paragraph coherence.", "Attach structured metadata to chunks to enable hybrid metadata-filtered vector queries."]
                ),
            ],
            "quiz": [
                {"id": 1, "question": "Why does cosine similarity between two normalized vectors equal their dot product?", "options": ["Because normalized vectors have a magnitude (length) of exactly 1.0, simplifying the denominator to 1", "Because cosine similarity is an obsolete metric that ignores vector direction", "Because dot products are only calculated in 2-dimensional space", "Because normalized vectors contain only positive integers"], "correct_index": 0},
                {"id": 2, "question": "What is the primary advantage of Approximate Nearest Neighbor (ANN) search algorithms like HNSW over exact flat k-NN search?", "options": ["ANN guarantees 100% mathematical recall accuracy across infinite datasets", "ANN achieves sub-linear search latency (O(log N)) by navigating graph structures instead of comparing against every vector (O(N))", "ANN eliminates the need for vector embeddings entirely", "ANN compresses vectors into raw ASCII text"], "correct_index": 1},
                {"id": 3, "question": "Why is chunk overlap (e.g. 50-100 characters) critical when splitting documents into smaller chunks for RAG?", "options": ["To make the vector database file as large as possible", "To prevent loss of contextual meaning and split phrases that fall precisely across chunk boundaries", "To trick the LLM into thinking it read multiple different documents", "To ensure chunks always contain an even number of tokens"], "correct_index": 1},
                {"id": 4, "question": "What is the primary function of metadata filtering in a vector database query?", "options": ["To re-write the user's natural language question into SQL", "To restrict the vector search space strictly to documents matching specific criteria (e.g. user_id, date, source) before or after similarity calculation", "To delete outdated vector embeddings automatically", "To translate vectors from one language to another"], "correct_index": 1},
                {"id": 5, "question": "What does MTEB stand for in the context of evaluating vector embedding models?", "options": ["Massive Text Embedding Benchmark", "Modern Transformer Evaluation Binary", "Multi-Token Execution Budget", "Modular Text Extraction Backend"], "correct_index": 0},
            ]
        },
        {
            "day_number": 3,
            "title": "Day 3: Production Retrieval-Augmented Generation (RAG) Pipelines",
            "subtopics": [
                (
                    "Standard RAG vs Production RAG Architecture",
                    "Diagnose the core failure modes of basic naive RAG: irrelevant retrieval, context fragmentation, hallucination despite retrieval, and context dilution ('lost in the middle'). Architect end-to-end production RAG pipelines featuring query pre-processing, multi-vector indexing, contextual compression, and strict hallucination guardrails in the synthesis prompt.",
                    ["Identify and diagnose common failure modes in basic retrieval-augmented generation.", "Design grounding system prompts that prevent hallucinated extrapolation.", "Structure modular RAG pipelines with clear retrieval, ranking, and synthesis boundaries."]
                ),
                (
                    "Query Transformation, Hybrid Search & Re-Ranking",
                    "Maximize retrieval precision. Implement query transformation techniques: Sub-Question Decomposition (breaking complex queries into distinct sub-queries) and Hypothetical Document Embeddings (HyDE). Combine dense semantic vector search with sparse keyword search (BM25) using Reciprocal Rank Fusion (RRF). Apply Cross-Encoder re-rankers (Cohere Re-rank, BGE-Reranker) to score document-query relevance with full self-attention.",
                    ["Implement HyDE to retrieve relevant documents when user queries are terse or abstract.", "Merge keyword search and vector search using Reciprocal Rank Fusion (RRF).", "Filter out false-positive chunks by applying Cross-Encoder re-ranking models."]
                ),
                (
                    "Contextual Compression & Source Citation Synthesis",
                    "Optimize context window efficiency and auditable accuracy. Implement contextual compression to extract only the specific sentences relevant to the query from long retrieved chunks. Prompt the LLM to generate strict inline citations referencing specific document identifiers and page numbers. Build post-generation citation verification modules that verify every claimed quote exists verbatim in retrieved sources.",
                    ["Compress retrieved context chunks to minimize prompt token bloat and inference latency.", "Synthesize professional responses featuring verified inline citations.", "Implement programmatic checks that audit LLM citations against ground-truth context chunks."]
                ),
            ],
            "quiz": [
                {"id": 1, "question": "What is the 'Lost in the Middle' phenomenon observed in transformer LLMs during RAG synthesis?", "options": ["Models delete tokens in the middle of long words", "Models show higher recall for information located at the very beginning or end of their input context, frequently ignoring relevant data placed in the middle", "Vector databases lose 50% of embeddings during indexing", "The middle layer of neural networks experiences zero gradient flow"], "correct_index": 1},
                {"id": 2, "question": "How does Hypothetical Document Embeddings (HyDE) improve search retrieval?", "options": ["It generates a hypothetical answer to the question using an LLM, then uses that answer's embedding to search the vector space for real documents", "It deletes hypothetical questions from the database", "It encrypts document chunks with random salts", "It forces the user to provide their own document embeddings"], "correct_index": 0},
                {"id": 3, "question": "What is the key structural difference between a Bi-Encoder (standard embedding model) and a Cross-Encoder (re-ranker)?", "options": ["Bi-encoders cannot process English text", "Bi-encoders embed query and document independently into vectors; Cross-encoders process query and document simultaneously through all attention layers", "Cross-encoders are 100x faster than Bi-encoders", "Bi-encoders require GPU clusters while Cross-encoders run on calculators"], "correct_index": 1},
                {"id": 4, "question": "In Reciprocal Rank Fusion (RRF), what does the formula RRF_Score = SUM(1 / (k + rank)) achieve?", "options": ["It calculates the exact cosine similarity between two documents", "It combines rankings from multiple disparate search algorithms (e.g. BM25 and vector search) without requiring score normalization", "It deletes duplicate records from a relational database table", "It calculates token latency in seconds"], "correct_index": 1},
                {"id": 5, "question": "What is the primary benefit of Contextual Compression in RAG pipelines?", "options": ["It compresses prompt context to reduce token costs, lower latency, and eliminate distracting irrelevant text", "It converts text into zip files on disk", "It replaces all vowels with asterisks", "It forces the LLM to output 5-word summaries only"], "correct_index": 0},
            ]
        },
        {
            "day_number": 4,
            "title": "Day 4: Tool Calling, Function Execution & Sandboxed Environments",
            "subtopics": [
                (
                    "Function Calling Protocols & Tool Declaration Schemas",
                    "Turn passive LLMs into active agents. Master the function calling protocol (OpenAI, Gemini). Define tool declarations using standard JSON Schema (tool name, description, parameter types, enums, required fields). Understand how the model decides when to return a standard text completion versus a structured tool call request. Parse tool call arguments, execute native code, and format tool results into tool-role messages.",
                    ["Write clean, descriptive JSON Schema declarations for custom Python functions.", "Handle LLM tool call payloads, argument parsing, and tool execution lifecycles.", "Format tool observations correctly back into conversation context to resume generation."]
                ),
                (
                    "Building External Tool Integrations (Search, SQL & APIs)",
                    "Equip agents with real-world utility. Build production-grade tool integrations: live web search (DuckDuckGo, Tavily), read-only SQL query execution with automatic schema introspection, and external REST API consumers. Enforce strict safety guardrails on database tools: enforcing SELECT statements only, read-only database connections, statement execution timeouts, and result set row limits to protect server memory.",
                    ["Integrate live internet search capabilities into autonomous agent loops.", "Safely equip agents with read-only SQL querying tools with strict execution constraints.", "Build robust API client tools that handle pagination and rate limits."]
                ),
                (
                    "Error Recovery, Hallucinated Tool Handling & Sandboxing",
                    "Build resilient tool execution engines. Handle common real-world failures: models calling nonexistent functions, passing invalid arguments that fail Pydantic validation, or tools throwing network exceptions. Instead of crashing, capture exception tracebacks, format them into helpful natural language error messages, and feed them back to the agent so it can self-correct. Sandbox arbitrary code execution tools in isolated environments.",
                    ["Implement self-healing tool execution wrappers that intercept exceptions and prompt the agent to self-correct.", "Validate tool call arguments with Pydantic before invocation to block bad inputs.", "Isolate untrusted code execution inside restricted containerized or subprocess sandboxes."]
                ),
            ],
            "quiz": [
                {"id": 1, "question": "In the OpenAI/Gemini function calling protocol, what actually executes the underlying Python tool code?", "options": ["The LLM neural network executes the Python code internally in its attention weights", "The client application/server hosting the code receives the tool call schema from the model, executes the function locally, and returns the result", "The cloud GPU cluster running the LLM executes the code in a remote sandbox", "A browser extension running on the user's laptop"], "correct_index": 1},
                {"id": 2, "question": "What is the most effective defense against an AI agent executing destructive SQL queries (e.g. DROP TABLE) when given database querying tools?", "options": ["Asking the LLM politely in the system prompt to only run safe queries", "Connecting the tool using a database user granted strictly read-only permissions (SELECT only) at the database engine level", "Changing the database file extension from .db to .txt", "Limiting user prompts to 10 words"], "correct_index": 1},
                {"id": 3, "question": "Why is the 'description' field in a tool's JSON Schema declaration critical to agent performance?", "options": ["It is printed in the terminal console when the script boots", "The LLM reads the description to determine what the tool does and decide whether calling it will help answer the user's request", "It is used by the database to index the tool's source code", "It sets the timeout duration of the function"], "correct_index": 1},
                {"id": 4, "question": "When an agent passes invalid arguments to a tool, what is the best architectural recovery strategy?", "options": ["Immediately crash the entire backend service with an unhandled exception", "Intercept the validation error and return a detailed error message as the tool's observation, allowing the model to correct its call", "Guess random argument values and rerun the tool silently", "Delete the conversation history and start from scratch"], "correct_index": 1},
                {"id": 5, "question": "What is the primary risk of allowing an AI agent to execute arbitrary Python code via a native eval() or exec() tool without sandboxing?", "options": ["The script might print duplicate messages", "An attacker could manipulate the agent via prompt injection to delete files, execute malicious shell commands, or exfiltrate private credentials", "The agent might change the Python version installed on the computer", "eval() only works on floating point numbers"], "correct_index": 1},
            ]
        },
        {
            "day_number": 5,
            "title": "Day 5: Autonomous Agent Architectures: ReAct & Plan-and-Solve",
            "subtopics": [
                (
                    "The ReAct Framework (Reasoning + Acting)",
                    "Implement the classic autonomous agent pattern: ReAct. Explore the cognitive loop: Thought (verbal reasoning over current state) -> Action (selecting a tool) -> Action Input (providing tool parameters) -> Observation (ingesting tool output) -> Reflection -> Final Answer. Build a clean, dependency-free ReAct execution engine in pure Python. Enforce iteration limits to prevent infinite execution loops and runaway API costs.",
                    ["Build a pure Python ReAct agent execution loop from scratch.", "Parse reasoning thoughts and tool actions using robust string and schema parsers.", "Implement iteration counters and cost guardrails to terminate runaway loops."]
                ),
                (
                    "Plan-and-Solve Prompting & Task Decomposition",
                    "Overcome myopic decision-making in complex multi-step objectives. Understand why step-by-step reaction often wanders off-track. Implement the Plan-and-Solve architecture: (1) Planner Agent decomposes a complex objective into an explicit list of sub-tasks, (2) Executor Agent iterates through the plan executing actions, (3) Re-planner updates remaining tasks based on intermediate findings. Contrast linear execution with tree-of-thought exploration.",
                    ["Implement separate Planner and Executor cognitive roles for complex problem solving.", "Decompose ambiguous high-level goals into ordered, testable sub-tasks.", "Enable dynamic re-planning when intermediate tool executions produce unexpected data."]
                ),
                (
                    "Agent Memory Architectures: Short-Term, Long-Term & Episodic",
                    "Endow agents with stateful persistence. Architect multi-tiered memory systems: Working Memory (current execution stack and tool observations), Short-Term Conversational Memory (sliding context buffers with automated LLM summarization of older dialogue turns), and Long-Term Episodic Memory (persisting past goals, user preferences, and solutions in vector databases for semantic retrieval across sessions).",
                    ["Maintain multi-turn conversation memory without exceeding token context limits.", "Implement automated conversation summarizers that compress historical dialogue.", "Store and retrieve past agent experiences and user profiles using episodic vector memory."]
                ),
            ],
            "quiz": [
                {"id": 1, "question": "In the ReAct agent framework, what is the specific purpose of the 'Thought' step before each 'Action'?", "options": ["It logs an error message to the system kernel", "It forces the model to articulate verbal reasoning over previous observations and deliberate on which tool to invoke next", "It renders the visual user interface in HTML", "It charges the user's credit card"], "correct_index": 1},
                {"id": 2, "question": "What is the primary advantage of the Plan-and-Solve agent architecture over a basic ReAct loop for complex research tasks?", "options": ["Plan-and-Solve requires zero tokens to run", "It decomposes the broad goal into an overarching roadmap first, avoiding myopic local decisions and looping behaviors", "It eliminates the need for tool execution", "It can only be used with local open-source models"], "correct_index": 1},
                {"id": 3, "question": "Why is an iteration limit (e.g. max_steps = 10) essential in any autonomous agent execution loop?", "options": ["To comply with international Python programming laws", "To prevent infinite loops from draining API token budgets and locking up server compute indefinitely", "Because Python cannot count higher than 10", "To ensure all answers contain exactly 10 words"], "correct_index": 1},
                {"id": 4, "question": "How does a Conversation Summary Memory buffer maintain long dialogues within fixed context windows?", "options": ["It deletes all vowels from user messages", "It progressively condenses older conversation turns into a running semantic summary while preserving recent messages verbatim", "It stores messages on floppy disks", "It forces the user to re-type their initial question"], "correct_index": 1},
                {"id": 5, "question": "What is 'Episodic Memory' in an autonomous agent system?", "options": ["The RAM currently in use by the operating system", "A persistent memory store (often in a vector DB) that preserves past experiences, task outcomes, and user preferences across multiple sessions", "A memory that resets every 5 minutes", "Memory dedicated solely to playing video clips"], "correct_index": 1},
            ]
        },
        {
            "day_number": 6,
            "title": "Day 6: Multi-Agent Orchestration, State Graphs & Governance",
            "subtopics": [
                (
                    "Multi-Agent Collaboration Patterns",
                    "Scale single agents into specialized agent teams. Explore collaboration topologies: Supervisor-Worker (central router agent delegates subtasks to specialized researcher, writer, and coder agents), Sequential Handoff (assembly line pipeline), and Multi-Agent Debate (opposing agents critique and refine outputs to minimize hallucination). Define explicit agent communication schemas and data contracts.",
                    ["Architect hierarchical Supervisor-Worker multi-agent teams.", "Implement agent debate protocols that cross-examine findings before final delivery.", "Design clear JSON data handoff contracts between specialized agents."]
                ),
                (
                    "Stateful Agent Graphs with LangGraph / Finite State Machines",
                    "Tame non-deterministic LLMs with deterministic execution graphs. Model agent workflows as stateful graphs: State schemas (shared TypedDict context), Nodes (agent actions or tool invocations), and Conditional Edges (routing logic based on output evaluation). Implement cyclic loops (e.g. Code -> Test -> Fail -> Re-code -> Test -> Pass). Incorporate Human-in-the-Loop checkpoints to gate sensitive actions (e.g. sending emails or issuing payments).",
                    ["Build deterministic cyclic state graphs with conditional routing logic.", "Implement automated evaluation loops that iterate until quality criteria are met.", "Integrate human-in-the-loop approval gates for mission-critical agent actions."]
                ),
                (
                    "Safety Guardrails, Content Moderation & Cost Governance",
                    "Deploy AI agents safely in enterprise settings. Implement multi-layered guardrails (NeMo Guardrails, Llama Guard): PII redaction (masking credit cards, phone numbers, emails), topic boundary enforcement (preventing agents from answering off-topic queries), and hallucination checks. Implement operational cost governance: tracking token expenditures per user, per-session rate limits, and hard budget circuit breakers.",
                    ["Redact Personally Identifiable Information (PII) before passing text to cloud LLM APIs.", "Implement dual-layer guardrails checking both inbound prompts and outbound answers.", "Enforce token quotas and circuit breakers to prevent runaway billing spikes."]
                ),
            ],
            "quiz": [
                {"id": 1, "question": "In a Supervisor-Worker multi-agent pattern, what is the primary role of the Supervisor agent?", "options": ["To execute all low-level code directly", "To analyze the user request, break it down, route subtasks to specialized worker agents, and synthesize the final result", "To monitor CPU hardware temperature", "To act as a database backup service"], "correct_index": 1},
                {"id": 2, "question": "What is the key advantage of modeling an agentic workflow as a state graph (like LangGraph) rather than an unconstrained while-loop?", "options": ["State graphs allow deterministic control flow, explicit state schemas, conditional branching, and checkpointing", "State graphs run without needing an internet connection", "State graphs eliminate the need for API keys", "State graphs convert Python code into assembly language"], "correct_index": 0},
                {"id": 3, "question": "What is a 'Human-in-the-Loop' (HITL) checkpoint in an agentic workflow?", "options": ["A requirement that a human manually types all LLM tokens", "A designated state graph interrupt where execution pauses until a human operator approves, edits, or rejects a sensitive action", "A captcha test shown to the LLM to verify it is human", "A physical button on the EC2 server chassis"], "correct_index": 1},
                {"id": 4, "question": "What is the primary function of a PII redaction guardrail in enterprise AI deployments?", "options": ["To replace all numbers with emojis", "To detect and mask sensitive user data (passwords, Aadhaar/SSN, payment cards) before prompts reach external cloud APIs", "To increase the cost of API inference", "To translate sensitive documents into Latin"], "correct_index": 1},
                {"id": 5, "question": "In cost governance, what is an 'API circuit breaker'?", "options": ["A physical fuse in the datacenter electrical panel", "An automated programmatic monitor that halts further LLM requests if a predefined monetary or token threshold is exceeded", "A tool that breaks long words into syllables", "A router that alternates between WiFi and Ethernet"], "correct_index": 1},
            ]
        },
        {
            "day_number": 7,
            "title": "Day 7: Production Deployment, Observability & Evaluation of AI Agents",
            "subtopics": [
                (
                    "Automated Evaluation & LLM-as-a-Judge Frameworks",
                    "Establish rigorous quality benchmarks for stochastic AI agents. Move beyond manual inspection. Implement automated evaluation frameworks (Ragas, DeepEval). Master core quantitative metrics: Faithfulness (hallucination detection against retrieved context), Answer Relevance, Context Precision, and Tool Calling Accuracy. Set up automated regression test suites that run in CI/CD before deploying agent updates.",
                    ["Evaluate RAG and agent systems quantitatively using Ragas and DeepEval metrics.", "Implement LLM-as-a-Judge evaluation prompts with calibrated scoring rubrics.", "Establish automated regression gates in CI/CD to prevent quality degradation across prompt updates."]
                ),
                (
                    "Observability, Tracing & Latency Optimization",
                    "Monitor multi-step agent reasoning in production. Instrument agent applications with distributed tracing (LangSmith, Phoenix/Arize, OpenTelemetry). Trace execution spans across nested tool calls, retrievals, and LLM calls. Measure token throughput and Time-to-First-Token (TTFT). Implement semantic caching (GPTCache, Redis) to serve instantaneous answers to recurring semantic queries, slashing API latency and cost.",
                    ["Instrument production agent pipelines with full distributed execution traces.", "Diagnose latency bottlenecks across vector retrieval, external tools, and model generation.", "Deploy semantic caching to serve instant responses for semantically similar user queries."]
                ),
                (
                    "Serving Agentic APIs with FastAPI & Dockerized EC2 Deployment",
                    "Package and deploy autonomous agent applications. Build high-performance asynchronous web APIs using FastAPI. Implement Server-Sent Events (SSE) to stream real-time reasoning steps, tool execution statuses, and generated answer tokens to web clients. Containerize the application using Docker, secure API keys in production .env files, and deploy behind an Nginx reverse proxy on an AWS EC2 instance.",
                    ["Build asynchronous FastAPI endpoints streaming agent thoughts and tokens via Server-Sent Events.", "Containerize agent microservices with Docker for reproducible production deployment.", "Deploy containerized AI agent APIs on AWS EC2 behind an Nginx reverse proxy."]
                ),
            ],
            "quiz": [
                {"id": 1, "question": "In RAG evaluation with frameworks like Ragas, what does the 'Faithfulness' metric measure?", "options": ["How quickly the model responds to queries in milliseconds", "The proportion of claims in the generated answer that can be directly inferred from the retrieved context, penalizing hallucinations", "Whether the user trusts the brand providing the service", "How closely the output matches a standard dictionary definition"], "correct_index": 1},
                {"id": 2, "question": "What is the primary benefit of streaming agent progress to frontend users via Server-Sent Events (SSE)?", "options": ["It eliminates the need for an SSL certificate", "It provides immediate visual feedback (showing intermediate thoughts and tokens) so users don't face a blank screen during long reasoning loops", "It compresses video files faster than WebSockets", "It allows the client to edit the backend database directly"], "correct_index": 1},
                {"id": 3, "question": "How does 'Semantic Caching' differ from traditional HTTP key-value caching for LLM applications?", "options": ["Traditional caching matches exact string keys; semantic caching compares vector embeddings to return cached answers for semantically equivalent questions", "Semantic caching only works on mobile devices", "Traditional caching requires GPU hardware", "Semantic caching deletes data every 60 seconds"], "correct_index": 0},
                {"id": 4, "question": "What does Time-to-First-Token (TTFT) measure in an LLM API service?", "options": ["The total time required to train the foundation model from scratch", "The elapsed time between the client sending a request and receiving the very first token of the response stream", "The time taken to save a prompt to an SQLite database", "The duration of an SSL handshake"], "correct_index": 1},
                {"id": 5, "question": "In distributed tracing for AI agents, what is a 'Span'?", "options": ["The total distance between the client laptop and the server", "A single timed unit of work representing an individual operation (such as an LLM call, a tool execution, or a vector retrieval) within a trace tree", "A memory leak in a Python script", "The total character count of a system prompt"], "correct_index": 1},
            ]
        },
    ]
}

FULL_STACK_DEVELOPMENT_COURSE = {
    "domain": "Full Stack Development",
    "title": "Full Stack Web Development: Modern Architecture, REST APIs & Cloud Deployment",
    "slug": "full-stack-web-development",
    "level": "Beginner to Intermediate",
    "estimated_hours": 18,
    "banner_gradient": "linear-gradient(135deg, #3B82F6, #1D4ED8)",
    "chapters": [
        {
            "day_number": 1,
            "title": "Day 1: Modern Web Architecture, Semantic HTML5 & Modern CSS Systems",
            "subtopics": [
                (
                    "Client-Server Architecture & The HTTP Request Lifecycle",
                    "Explore the foundational mechanics of the modern internet. Analyze the complete lifecycle of a web request: DNS resolution, TCP three-way handshake, TLS cryptographic negotiation, and HTTP/1.1 vs HTTP/2 multiplexing. Examine REST protocol semantics, distinguishing idempotent idempotent operations (GET, PUT, DELETE) from non-idempotent operations (POST, PATCH), and master HTTP status code families (2xx success, 3xx redirection, 4xx client errors, 5xx server faults).",
                    ["Trace the journey of a network packet from browser address bar to web server and back.", "Leverage HTTP caching headers (Cache-Control, ETag, If-None-Match) to optimize network bandwidth.", "Design RESTful URL paths adhering to uniform resource identification standards."]
                ),
                (
                    "Semantic HTML5, Accessibility (a11y) & The DOM Tree",
                    "Build web interfaces that are universally accessible and search-engine optimized. Replace unsemantic div-soup with semantic landmark tags (<header>, <nav>, <main>, <article>, <aside>, <footer>). Master WCAG 2.1 AA accessibility guidelines, color contrast ratios, keyboard tab navigation, and ARIA attributes (aria-label, aria-live). Understand how the browser parses markup into the Document Object Model (DOM) and accessibility tree.",
                    ["Construct clean, accessible document outlines using HTML5 landmark elements.", "Formulate form controls with explicitly paired <label> tags and accessible validation feedback.", "Conduct browser accessibility audits using Lighthouse and keyboard navigation checks."]
                ),
                (
                    "Modern CSS Layouts, Design Tokens & Tailwind Fundamentals",
                    "Architect scalable, maintainable CSS systems. Master one-dimensional layouts with Flexbox and two-dimensional matrix grid systems with CSS Grid. Learn to build custom design systems using CSS Custom Properties (variables) for design tokens (colors, typography, spacing, shadows). Transition from rigid pixel values to fluid responsive units (rem, clamp(), min(), max()). Explore utility-first CSS principles as embodied by modern frameworks like Tailwind CSS.",
                    ["Build complex multi-column responsive dashboard layouts with CSS Grid and Flexbox.", "Create dynamic, zero-runtime theme switchers (light/dark mode) using CSS Custom Properties.", "Apply mobile-first responsive design strategies without relying on bloated legacy frameworks."]
                ),
            ],
            "quiz": [
                {"id": 1, "question": "Which of the following HTTP methods is considered idempotent by REST standards?", "options": ["POST", "PATCH", "PUT", "CONNECT"], "correct_index": 2},
                {"id": 2, "question": "What is the primary architectural purpose of semantic HTML5 tags such as <main> and <nav>?", "options": ["They automatically apply built-in CSS styling animations to the page", "They communicate structural meaning to search engines and assistive screen readers", "They improve JavaScript execution speed by compiling into WebAssembly", "They bypass browser Content Security Policy restrictions"], "correct_index": 1},
                {"id": 3, "question": "In modern responsive CSS, what does the expression 'width: clamp(200px, 50vw, 800px)' do?", "options": ["It fixes the element width strictly at 50vw across all screens", "It throws an error because clamp() only accepts pixel values", "It sets a fluid width of 50vw bounded by a minimum of 200px and maximum of 800px", "It centers the element horizontally inside its grid container"], "correct_index": 2},
                {"id": 4, "question": "What is the difference between an HTTP 301 and an HTTP 302 redirect status code?", "options": ["301 indicates a permanent redirect that browsers cache; 302 indicates a temporary redirect", "301 is an internal server error; 302 is an authentication error", "301 is used only for image files; 302 is used for HTML pages", "301 requires HTTPS; 302 only works over unencrypted HTTP"], "correct_index": 0},
                {"id": 5, "question": "In Flexbox, what does the property 'justify-content' control compared to 'align-items'?", "options": ["justify-content aligns items along the cross axis; align-items along the main axis", "justify-content aligns items along the main axis; align-items along the cross axis", "Both properties perform identical operations along the vertical axis", "justify-content handles text justification inside paragraphs only"], "correct_index": 1},
            ]
        },
        {
            "day_number": 2,
            "title": "Day 2: Modern JavaScript & Frontend Engineering with React",
            "subtopics": [
                (
                    "Modern JavaScript (ES6+), Event Loop & Asynchronous Control",
                    "Deepen your understanding of JavaScript fundamentals. Master ES6+ features: destructuring, rest/spread operators, arrow functions, template literals, and optional chaining (?.), nullish coalescing (??). Explore the V8 engine architecture: call stack, memory heap, microtask queue (Promises), and macrotask queue (setTimeout). Write robust asynchronous code with async/await, handling concurrency with Promise.all and Promise.allSettled.",
                    ["Debug asynchronous timing bugs and race conditions using knowledge of the event loop.", "Write clean, readable functional code using ES6+ syntax and immutability patterns.", "Execute concurrent API calls safely using Promise.allSettled."]
                ),
                (
                    "React Fundamentals, JSX & Component Architecture",
                    "Transition from imperative DOM manipulation to declarative user interfaces. Understand how React's Virtual DOM computes diffs to minimize real DOM mutations. Build composable functional components, pass data via unidirectional props, handle synthetic events, and render lists efficiently using stable key attributes. Understand the build-time compilation of JSX to React.createElement using modern bundlers like Vite.",
                    ["Break down UI mockups into composable, single-responsibility React components.", "Manage data flow predictably from parent components to children via props.", "Avoid re-rendering bugs by providing stable, unique keys to dynamic list elements."]
                ),
                (
                    "State Management with React Hooks (useState, useEffect, useRef)",
                    "Master React's official hook primitives. Manage local state with useState, ensuring state updates are treated immutably. Handle component side effects, asynchronous subscriptions, and DOM lifecycles with useEffect. Understand the role of dependency arrays in preventing infinite re-render loops and stale closures. Use useRef to persist mutable values across renders and interact directly with native DOM nodes.",
                    ["Manage interactive UI state cleanly with functional updater functions in useState.", "Correctly specify dependency arrays in useEffect to prevent stale closures and memory leaks.", "Safely capture references to DOM elements using useRef."]
                ),
            ],
            "quiz": [
                {"id": 1, "question": "In the JavaScript event loop, which queue has higher execution priority after the current call stack clears?", "options": ["The Macrotask queue (setTimeout, setInterval)", "The Microtask queue (Promise callbacks, queueMicrotask)", "The RequestAnimationFrame queue", "The Garbage Collection queue"], "correct_index": 1},
                {"id": 2, "question": "Why should array indices generally be avoided as keys when rendering dynamic lists in React?", "options": ["React will throw a runtime syntax exception and crash", "Array indices can cause component state bugs and incorrect DOM recycling when items are reordered or filtered", "Array indices consume twice as much memory in the virtual DOM", "Vite bundler cannot compile JSX containing numeric keys"], "correct_index": 1},
                {"id": 3, "question": "What is the primary purpose of the cleanup function returned from a React useEffect hook?", "options": ["To delete the component from the browser history", "To clear timers, cancel pending network subscriptions, and clean up resources before unmounting or re-running", "To reset all useState variables back to their initial values", "To force an immediate browser page reload"], "correct_index": 1},
                {"id": 4, "question": "What does the JavaScript nullish coalescing operator (??) evaluate?", "options": ["It returns the right-hand operand only if the left-hand operand is strictly null or undefined", "It returns the right-hand operand if the left-hand operand is any falsy value (0, '', false)", "It compares whether two objects have identical memory references", "It performs a cryptographic hash comparison between two strings"], "correct_index": 0},
                {"id": 5, "question": "What distinguishes useRef from useState in React functional components?", "options": ["useRef can only store strings, whereas useState can store any type", "Updating a ref value (.current) does not trigger a component re-render, whereas calling a state setter does", "useRef cannot be used inside custom hooks", "useState values persist across page reloads automatically"], "correct_index": 1},
            ]
        },
        {
            "day_number": 3,
            "title": "Day 3: Backend Fundamentals & RESTful API Engineering with Python & Flask",
            "subtopics": [
                (
                    "WSGI Applications & The Flask Request/Response Lifecycle",
                    "Unpack Python web architectures. Understand the Web Server Gateway Interface (WSGI) standard that bridges production web servers (Nginx/Gunicorn) with Python web applications. Learn how Flask initializes application and request contexts. Explore Flask request objects (headers, form data, JSON payloads, query parameters) and response construction (jsonify, status codes, custom headers).",
                    ["Understand the boundary between web servers (WSGI) and Python application logic.", "Inspect inbound HTTP headers, cookies, and JSON payloads within Flask request contexts.", "Construct consistent, standardized JSON HTTP responses with proper status codes."]
                ),
                (
                    "Designing Idempotent RESTful APIs with JSON Payloads",
                    "Design production-grade REST APIs. Implement standard CRUD routing patterns, dynamic URL converters (<int:id>, <string:slug>), and query-string pagination (page, per_page). Enforce input validation, content-type verification (application/json), and handle errors with unified schema formats (e.g. {'status': 'error', 'message': '...'}). Master HTTP semantics for creation (201 Created with Location header) and validation failures (400 Bad Request, 422 Unprocessable Entity).",
                    ["Implement URL parameter converters to enforce type safety at the routing layer.", "Design uniform error response envelopes across all API endpoints.", "Structure clean pagination metadata (total_count, page, total_pages) for client consumption."]
                ),
                (
                    "Modular Architecture with Flask Blueprints & Middleware",
                    "Scale web applications from monolithic scripts into organized, maintainable architectures. Structure backend systems using Flask Blueprints to separate authentication, administration, and resource endpoints into discrete modules. Implement application middleware hooks: before_request (authentication checks, rate limits), after_request (security headers, CSP nonces), and teardown_request (database connection cleanup).",
                    ["Organize enterprise web applications into decoupled, testable Flask Blueprints.", "Centralize cross-cutting concerns (authentication gates, audit logging) in before_request hooks.", "Enforce security headers and clean up database connections in after_request hooks."]
                ),
            ],
            "quiz": [
                {"id": 1, "question": "What is the primary role of WSGI (Web Server Gateway Interface) in Python web deployments?", "options": ["To compile Python bytecode into C++ for faster execution", "To act as a standardized interface between web servers (e.g. Gunicorn/Nginx) and Python web applications", "To provide browser-based CSS styling templates", "To encrypt database passwords automatically"], "correct_index": 1},
                {"id": 2, "question": "Which HTTP status code is the most semantically appropriate when a new resource is successfully created via POST?", "options": ["200 OK", "201 Created", "204 No Content", "202 Accepted"], "correct_index": 1},
                {"id": 3, "question": "In Flask, what is the key advantage of using Blueprints?", "options": ["They replace the need for an underlying database", "They modularize routes, templates, and static assets into independent logical components", "They convert Flask synchronous routes into async Go routines", "They automatically eliminate all CSS specificity conflicts"], "correct_index": 1},
                {"id": 4, "question": "What happens if a client submits a POST request with malformed JSON to a Flask route expecting request.get_json()?", "options": ["Flask re-routes the user to the homepage", "Flask by default raises a 400 Bad Request HTTP exception unless silent=True is passed", "The server crashes and terminates the WSGI worker process", "The malformed JSON is automatically converted into an XML string"], "correct_index": 1},
                {"id": 5, "question": "Which Flask hook executes after every request, allowing you to append security headers to the outgoing response?", "options": ["@app.before_request", "@app.teardown_request", "@app.after_request", "@app.context_processor"], "correct_index": 2},
            ]
        },
        {
            "day_number": 4,
            "title": "Day 4: Relational Database Modeling, SQL & Data Integrity",
            "subtopics": [
                (
                    "Schema Normalization & Entity-Relationship Design",
                    "Design robust database architectures. Walk through relational normalization rules from First Normal Form (1NF: atomic values) through Third Normal Form (3NF: eliminating transitive dependencies). Define primary keys, composite keys, and foreign key relationships (1:1, 1:N, N:M junction tables). Master integrity constraints: NOT NULL, UNIQUE, CHECK, and cascade behavior (ON DELETE CASCADE, ON DELETE SET NULL).",
                    ["Eliminate data redundancy and update anomalies through relational normalization.", "Model many-to-many business relationships using normalized join tables.", "Enforce business rules directly in database DDL via CHECK constraints."]
                ),
                (
                    "Query Optimization, Multi-Table Joins & Indexing Strategies",
                    "Write high-performance SQL queries. Master relational joins: INNER JOIN, LEFT OUTER JOIN, and cross joins. Understand join cardinality and avoid cartesian explosion traps that duplicate financial data. Learn how B-tree indexes accelerate WHERE and ORDER BY lookups. Use EXPLAIN QUERY PLAN to detect full table scans (SCAN TABLE) and evaluate when covering indexes or composite indexes are warranted.",
                    ["Analyze execution plans to optimize slow queries and eliminate full table scans.", "Create composite B-tree indexes matching query predicate column ordering.", "Audit join output row counts to prevent metric inflation from multi-table joins."]
                ),
                (
                    "ACID Transactions, Concurrency & SQLite WAL Mode",
                    "Protect data integrity under concurrent traffic. Master ACID guarantees: Atomicity, Consistency, Isolation, and Durability. Implement database transactions with BEGIN, COMMIT, and ROLLBACK blocks. Understand race conditions (dirty reads, non-repeatable reads, lost updates). Configure SQLite Write-Ahead Logging (PRAGMA journal_mode=WAL) to enable simultaneous readers and writers without lock contention.",
                    ["Prevent financial race conditions using explicit database transactions with rollback safety.", "Configure SQLite WAL mode and busy timeouts for high-throughput concurrent production apps.", "Safely handle database deadlocks and concurrency locks in web services."]
                ),
            ],
            "quiz": [
                {"id": 1, "question": "What is the primary condition required for a relational database table to satisfy Third Normal Form (3NF)?", "options": ["It must have at least five columns and an auto-incrementing integer ID", "It must be in 2NF and contain no transitive functional dependencies of non-key attributes on the primary key", "All columns must store binary serialized JSON objects", "It must use a NoSQL key-value document store"], "correct_index": 1},
                {"id": 2, "question": "What does a LEFT JOIN return when a record in the left table has no matching row in the right table?", "options": ["The left row is completely omitted from the result set", "The query throws a foreign key constraint violation error", "The left row is returned with NULL values populated for all right table columns", "The query halts and prompts the user to insert the missing record"], "correct_index": 2},
                {"id": 3, "question": "In SQLite, what is the primary benefit of enabling Write-Ahead Logging (PRAGMA journal_mode=WAL)?", "options": ["It automatically encrypts the entire database file with AES-256", "It permits multiple reading processes to read concurrently while a writing process writes changes", "It compresses the database file to 10% of its original size", "It replaces SQL syntax with Python dictionary lookups"], "correct_index": 1},
                {"id": 4, "question": "Why does adding an index to every single column in a high-write database table harm overall performance?", "options": ["Indexes consume all CPU cache memory and prevent SQL queries from running", "Every INSERT, UPDATE, or DELETE operation must synchronously update all associated B-tree index structures", "Indexes only function properly when there are fewer than 100 rows in the table", "Database connections cannot open when more than 3 indexes exist"], "correct_index": 1},
                {"id": 5, "question": "Which property of ACID ensures that if any operation within a transaction fails, the entire transaction is rolled back leaving data unchanged?", "options": ["Atomicity", "Consistency", "Isolation", "Durability"], "correct_index": 0},
            ]
        },
        {
            "day_number": 5,
            "title": "Day 5: Authentication, Authorization & Web Application Security",
            "subtopics": [
                (
                    "Secure Password Hashing & Salted Cryptographic Storage",
                    "Defend user credentials against credential stuffing and database dumps. Understand why plain text, MD5, and fast cryptographic hashes (SHA-256) are fundamentally unsafe for password storage due to high-speed GPU dictionary attacks. Master adaptive key-derivation functions (Argon2, bcrypt, PBKDF2). Implement salted hashing using Werkzeug/bcrypt and configure appropriate computational work factors.",
                    ["Implement salted, slow hashing functions using generate_password_hash and check_password_hash.", "Understand how unique salts defeat pre-computed rainbow table attacks.", "Configure adaptive computational work factors to withstand evolving GPU brute-force hardware."]
                ),
                (
                    "Session-Based Auth vs Stateless JWT Tokens & Cookie Security",
                    "Architect web authentication mechanisms. Compare stateful server-side sessions stored in databases/Redis against stateless JSON Web Tokens (JWT). Learn the anatomy of a JWT (Header, Payload, Signature) and token verification. Harden web cookies by configuring security flags: HttpOnly (mitigating XSS extraction), Secure (transmitting strictly over HTTPS), and SameSite=Strict/Lax (mitigating CSRF).",
                    ["Configure hardened session cookies with HttpOnly, Secure, and SameSite attributes.", "Implement signed JWT tokens with claims (sub, exp, iat) and refresh token rotation.", "Choose between stateful sessions and stateless tokens based on application scale and revocation needs."]
                ),
                (
                    "Defending the OWASP Top 10 (SQLi, XSS, CSRF & CSP)",
                    "Harden full-stack web applications against common web exploits. Eliminate SQL Injection (SQLi) using strictly parameterized database queries. Prevent Cross-Site Scripting (XSS) via context-aware output escaping and Content Security Policy (CSP) headers with cryptographic nonces. Defend against Cross-Site Request Forgery (CSRF) using synchronized anti-CSRF tokens. Secure file upload endpoints against directory traversal and remote code execution.",
                    ["Eliminate SQL injection vulnerabilities by enforcing parameterized queries across all database drivers.", "Deploy a strict Content Security Policy (CSP) header using dynamic nonces to block inline script injection.", "Validate and sanitize user input and file uploads to prevent path traversal and execution exploits."]
                ),
            ],
            "quiz": [
                {"id": 1, "question": "What is the primary vulnerability of storing passwords using standard SHA-256 hashing without a salt?", "options": ["SHA-256 produces variable length hashes that crash databases", "Attackers can instantly reverse identical passwords using precomputed rainbow tables and GPU brute-forcing", "SHA-256 only works on ASCII characters", "The algorithm expires after 10,000 uses"], "correct_index": 1},
                {"id": 2, "question": "What security protection does setting the 'HttpOnly' flag on an authentication session cookie provide?", "options": ["It forces the cookie to be sent only over unencrypted HTTP connections", "It prevents client-side JavaScript (e.g. document.cookie) from accessing the cookie, protecting it from XSS theft", "It ensures the cookie automatically deletes itself after 5 minutes", "It encrypts the entire HTTP body payload with AES-128"], "correct_index": 1},
                {"id": 3, "question": "Which of the following database queries is vulnerable to SQL Injection?", "options": ["cursor.execute('SELECT * FROM users WHERE email = ?', (user_email,))", "cursor.execute(f'SELECT * FROM users WHERE email = \\'{user_email}\\'')", "cursor.execute('SELECT * FROM users WHERE email = :email', {'email': user_email})", "conn.execute('SELECT * FROM users WHERE id = ?', [user_id])"], "correct_index": 1},
                {"id": 4, "question": "What is the primary mechanism of a Cross-Site Request Forgery (CSRF) attack?", "options": ["An attacker reads your database password directly over the network", "A malicious website tricks an authenticated user's browser into sending unauthorized requests to a trusted application", "An attacker floods the server with UDP packets to knock it offline", "An attacker injects malicious SQL into a search bar"], "correct_index": 1},
                {"id": 5, "question": "In a modern Content Security Policy (CSP), what is the function of a 'nonce'?", "options": ["A static password hardcoded into the HTML head tag", "A cryptographically random, single-use token generated per HTTP response that permits only authorized inline scripts to execute", "An integer counter tracking the number of page views", "A hash of the database connection string"], "correct_index": 1},
            ]
        },
        {
            "day_number": 6,
            "title": "Day 6: Full-Stack Integration, State Management & Asynchronous Data Pipelines",
            "subtopics": [
                (
                    "Frontend-Backend Communication with Fetch/Axios & Error Boundaries",
                    "Bridge the gap between frontend clients and backend APIs. Build reusable API client abstractions using Fetch API or Axios with interceptors for token injection and automatic 401 redirect handling. Manage asynchronous loading states, empty collection states, and error toasts. Implement React Error Boundaries to catch unhandled JavaScript runtime exceptions and display graceful recovery interfaces.",
                    ["Construct reusable HTTP client wrappers with request and response interceptors.", "Manage loading, error, and data states cleanly in user interface components.", "Isolate UI crashes using React Error Boundaries to protect user sessions."]
                ),
                (
                    "Multipart Form Submissions, File Uploads & Asset Storage",
                    "Handle file uploads securely and reliably. Understand multipart/form-data encoding and boundary streams. Implement server-side validation: checking file size limits, validating allowed MIME types and file extensions, inspecting magic bytes/signatures, and generating secure random UUID filenames (preventing directory traversal attacks). Serve user-uploaded assets with proper Content-Disposition and security headers.",
                    ["Accept and process multipart file streams safely on the web backend.", "Validate file uploads using file signatures (magic bytes) rather than relying solely on file extensions.", "Store uploads using randomized UUID paths to prevent filename collisions and traversal attacks."]
                ),
                (
                    "Optimistic UI Updates & Real-Time State Synchronization",
                    "Deliver ultra-responsive user experiences. Implement optimistic UI patterns: immediately updating client-side state when a user triggers an action (e.g. toggling a task checkbox, liking a post), while simultaneously dispatching the asynchronous API mutation. Implement robust rollback handlers to revert UI state if the backend rejects the transaction. Explore real-time synchronization patterns via Server-Sent Events (SSE) and WebSockets.",
                    ["Implement optimistic UI updates that provide zero-latency feedback to users.", "Build rollback mechanisms that restore accurate state if backend operations fail.", "Understand the trade-offs between polling, Server-Sent Events (SSE), and bidirectional WebSockets."]
                ),
            ],
            "quiz": [
                {"id": 1, "question": "What is the primary UX advantage of implementing 'optimistic UI updates' in a web application?", "options": ["It eliminates the need for a backend database", "The interface responds instantly to user interactions without waiting for network round-trip latency", "It automatically encrypts user data before sending it over the wire", "It decreases the size of bundle files generated by Vite"], "correct_index": 1},
                {"id": 2, "question": "Why is checking only the file extension (e.g. .jpg) insufficient when validating user file uploads on the backend?", "options": ["File extensions cannot be read in Python", "An attacker can rename a malicious executable script (.php, .sh, .exe) with a .jpg extension to bypass the check", "Browsers automatically strip file extensions from uploads", "File extensions are limited to 3 characters in modern operating systems"], "correct_index": 1},
                {"id": 3, "question": "In Axios, what is the role of a 'response interceptor'?", "options": ["To inspect or transform responses, or globally handle HTTP error codes (like 401 Unauthorized), before .then() or .catch() execute", "To compress outgoing request images into WebP format", "To prevent the browser from closing during file downloads", "To translate English error messages into foreign languages"], "correct_index": 0},
                {"id": 4, "question": "What HTTP encoding header is required when sending binary file data alongside text fields in an HTML form submission?", "options": ["application/x-www-form-urlencoded", "text/plain", "multipart/form-data", "application/octet-stream-only"], "correct_index": 2},
                {"id": 5, "question": "What is the primary role of a React Error Boundary?", "options": ["To prevent CSS layout shifts", "To catch JavaScript runtime errors anywhere in its child component tree and display a fallback UI instead of crashing the whole app", "To validate backend SQL schema migrations", "To terminate user sessions when a network disconnects"], "correct_index": 1},
            ]
        },
        {
            "day_number": 7,
            "title": "Day 7: Production Deployment, Linux/EC2 Infrastructure & DevOps",
            "subtopics": [
                (
                    "Linux Server Administration & AWS EC2 Instance Hardening",
                    "Deploy applications to cloud infrastructure. Navigate Linux servers over SSH. Manage system users, file permissions (chmod, chown), and isolate web app directories (/var/www/apps/). Configure firewall rules using Uncomplicated Firewall (ufw) and AWS Security Groups (exposing ports 22, 80, 443 only). Manage sensitive environment variables securely using isolated .env files with restricted permissions (chmod 600).",
                    ["Secure and configure a cloud Ubuntu Linux server on AWS EC2.", "Enforce least-privilege file permissions on web application root directories.", "Configure UFW and AWS security group firewalls against port scanners and intrusion attempts."]
                ),
                (
                    "Reverse Proxying with Nginx & SSL/TLS Configuration",
                    "Configure Nginx as a high-performance reverse proxy and web server. Write robust Nginx server blocks that terminate SSL/TLS encryption, route traffic to internal application servers (http://127.0.0.1:5000), serve static files directly with gzip compression, buffer slow client requests, and enforce HTTP-to-HTTPS redirection. Obtain and automate free SSL/TLS certificates via Let's Encrypt and Certbot.",
                    ["Write production Nginx configuration blocks for reverse proxying to Python WSGI backends.", "Offload static asset delivery to Nginx to free up application worker processes.", "Automate SSL/TLS certificate renewal using Certbot and Let's Encrypt."]
                ),
                (
                    "Process Management with Gunicorn & Systemd Services",
                    "Run Python web applications continuously in production. Configure Gunicorn WSGI application servers: calculate worker pools based on CPU cores ((2 * CPU) + 1), handle request timeouts, and configure log file destinations. Write a Linux Systemd service unit (/etc/systemd/system/app.service) to daemonize the application, guarantee automatic restarts on failure or server reboot, and monitor health logs with journalctl.",
                    ["Configure production Gunicorn worker processes and logging parameters.", "Create and manage persistent Linux Systemd service units.", "Monitor live production application logs and diagnose faults using journalctl."]
                ),
            ],
            "quiz": [
                {"id": 1, "question": "What is the recommended rule of thumb for calculating the optimal number of Gunicorn worker processes on a dedicated server?", "options": ["1 worker per 1,000 users", "(2 * Number of CPU Cores) + 1", "Exactly 100 workers regardless of hardware", "1 worker per database table"], "correct_index": 1},
                {"id": 2, "question": "In production, why is Nginx placed in front of Gunicorn as a reverse proxy rather than exposing Gunicorn directly to the public internet?", "options": ["Nginx is required to execute Python code", "Nginx efficiently handles slow clients, SSL termination, static file caching, and protects Gunicorn from connection exhaustion attacks", "Gunicorn cannot bind to TCP ports", "AWS EC2 blocks all traffic not originating from Nginx"], "correct_index": 1},
                {"id": 3, "question": "In a Linux systemd service unit file, what does the directive 'Restart=always' ensure?", "options": ["The server restarts the entire operating system every 10 minutes", "Systemd automatically relaunches the process if it crashes or terminates unexpectedly", "The process is restarted every time a git push occurs", "All database records are purged on startup"], "correct_index": 1},
                {"id": 4, "question": "Which Linux command displays live, real-time log output for a systemd service named 'internship.service'?", "options": ["journalctl -u internship.service -f", "cat /var/log/syslog --watch", "systemctl status internship --tail", "gunicorn --show-logs internship.service"], "correct_index": 0},
                {"id": 5, "question": "What permission setting represents 'chmod 600 .env' in Linux?", "options": ["Read, write, and execute permissions for everyone", "Read and write permissions for the file owner only; no access for group or others", "Read-only access for the entire operating system", "Execute-only access for web server daemons"], "correct_index": 1},
            ]
        },
    ]
}

PYTHON_AUTOMATION_COURSE = {
    "domain": "Python Automation",
    "title": "Python Automation & Web Scraping: Production Pipelines & Cloud Daemons",
    "slug": "python-automation-engineering",
    "level": "Beginner to Intermediate",
    "estimated_hours": 16,
    "banner_gradient": "linear-gradient(135deg, #10B981, #047857)",
    "chapters": [
        {
            "day_number": 1,
            "title": "Day 1: Modern Python Scripting, File I/O & OS-Level Automation",
            "subtopics": [
                (
                    "Pathlib, Cross-Platform File Systems & Directory Walks",
                    "Upgrade your filesystem automation skills. Replace legacy, fragile os.path string concatenations with object-oriented pathlib.Path. Navigate directory structures safely across Windows and Linux. Perform recursive file discovery with rglob(), batch file renaming, and extract file metadata (size, created/modified timestamps). Build automated file tidying scripts that organize chaotic directories by file extension and date stamps.",
                    ["Write cross-platform filesystem scripts using object-oriented pathlib.Path.", "Execute recursive directory walks and batch file operations with rglob().", "Inspect and filter files based on system timestamps and byte sizes."]
                ),
                (
                    "Structured Data Parsing: JSON, CSV, YAML & Config Management",
                    "Parse and manipulate diverse structured data feeds. Ingest and serialize nested JSON objects with proper encoding handling. Stream multi-gigabyte CSV transaction exports row-by-row using csv.DictReader to prevent server memory exhaustion. Parse YAML configuration files for automation settings, and isolate sensitive credentials using python-dotenv with strictly scoped environment variables.",
                    ["Stream large CSV files without memory bloat using csv.DictReader.", "Safely parse and format nested JSON and YAML configuration files.", "Secure automation secrets using environment variables and python-dotenv."]
                ),
                (
                    "Subprocess Management & Shell Command Orchestration",
                    "Command operating system utilities directly from Python. Use subprocess.run and subprocess.Popen safely: capture stdout and stderr streams, enforce non-zero exit code validation (check=True), and set execution timeouts to prevent hung processes from blocking servers. Eliminate critical shell injection vulnerabilities by passing command arguments as safe argument lists rather than raw strings with shell=True.",
                    ["Orchestrate external CLI tools and shell utilities safely from Python scripts.", "Capture and parse standard output and error streams programmatically.", "Prevent shell injection vulnerabilities by avoiding unsanitized shell=True calls."]
                ),
            ],
            "quiz": [
                {"id": 1, "question": "What is the primary architectural advantage of using 'csv.DictReader' over 'csv.reader' when parsing enterprise CSV files?", "options": ["It automatically compresses the CSV file into a zip archive", "It maps each row to a dictionary using header names as keys, preventing bugs when column orders change", "It loads all rows into GPU memory at once", "It translates text into French"], "correct_index": 1},
                {"id": 2, "question": "In Python's pathlib module, what method recursively matches all files ending in '.log' across all nested subdirectories?", "options": ["Path.glob('*.log')", "Path.rglob('*.log')", "Path.find_all('*.log')", "Path.scan_dir('.log')"], "correct_index": 1},
                {"id": 3, "question": "Why is 'subprocess.run(..., shell=True)' considered dangerous when incorporating user-provided input?", "options": ["It runs 100x slower than shell=False", "It passes input directly to the system shell interpreter, exposing the machine to arbitrary command injection exploits", "It automatically deletes the user's home directory", "It only works on 32-bit Windows machines"], "correct_index": 1},
                {"id": 4, "question": "What happens if a command executed via 'subprocess.run(cmd, check=True)' returns an exit code of 1?", "options": ["Python prints a warning and continues running silently", "Python raises a CalledProcessError exception that can be caught in a try/except block", "The operating system reboots immediately", "The return code is converted to 0"], "correct_index": 1},
                {"id": 5, "question": "What is the purpose of passing 'timeout=30' to a 'subprocess.run()' invocation in an automation worker?", "options": ["To make the script pause for 30 seconds before starting", "To terminate the child process and raise a TimeoutExpired exception if it fails to finish within 30 seconds", "To limit CPU usage to 30%", "To set the process priority to low"], "correct_index": 1},
            ]
        },
        {
            "day_number": 2,
            "title": "Day 2: Web Scraping & HTML Parsing with BeautifulSoup & Requests",
            "subtopics": [
                (
                    "HTTP Client Engineering: Sessions, Headers & Resilient Retries",
                    "Build industrial-strength HTTP scrapers. Use requests.Session to maintain persistent TCP connections (HTTP Keep-Alive) and manage cookies across requests. Configure realistic browser headers (User-Agent, Accept, Accept-Language) to avoid naive bot blockers. Mount custom HTTP adapters with urllib3.util.retry.Retry to implement automatic exponential backoff retries when facing 429 Too Many Requests or intermittent 502/503 server errors.",
                    ["Maintain persistent TCP connections and session cookies using requests.Session.", "Configure realistic browser request headers to avoid automated anti-bot triggers.", "Implement exponential backoff retry adapters to survive intermittent network faults."]
                ),
                (
                    "DOM Parsing, CSS Selectors & XPath with BeautifulSoup",
                    "Extract structured data from raw HTML trees. Compare parsing engines (lxml vs html.parser). Master concise CSS selector syntax with soup.select() and soup.select_one(). Navigate complex DOM hierarchies using relative traversal: parent, next_sibling, and find_previous. Extract link hrefs, image sources, and parse nested tabular data into clean Python dictionaries and lists.",
                    ["Extract target content accurately using concise CSS selectors in BeautifulSoup.", "Traverse complex DOM hierarchies using relative parent/sibling navigation methods.", "Parse structured HTML tables into standardized Python dictionaries."]
                ),
                (
                    "Anti-Bot Defense Navigation: Headers, Proxies & Rate Governance",
                    "Scrape sustainably and responsibly. Navigate modern rate limiters and Web Application Firewalls (WAF). Implement randomized jitter delays (random.uniform) between requests to avoid predictable bot cadence. Configure HTTP and SOCKS5 proxy pools to distribute outbound traffic. Parse and honor target site robots.txt files, identify honeypot links, and manage ethical scraping boundaries.",
                    ["Prevent automated IP bans using randomized jitter sleep intervals.", "Route scraper requests through HTTP and SOCKS5 proxy pools.", "Parse robots.txt directives and avoid hidden honeypot trap elements."]
                ),
            ],
            "quiz": [
                {"id": 1, "question": "What is the primary network advantage of using 'requests.Session()' over standalone 'requests.get()' calls in a loop?", "options": ["It uses dark mode styling for HTTP responses", "It reuses underlying TCP socket connections (Keep-Alive), eliminating repetitive TCP and TLS handshakes", "It bypasses all internet firewall rules", "It doubles the download speed of video files"], "correct_index": 1},
                {"id": 2, "question": "In BeautifulSoup, what is the difference between 'soup.find()' and 'soup.select()'?", "options": ["find() uses tag name and keyword filters; select() accepts standard CSS selector strings", "find() works only on XML; select() works only on JSON", "select() is deprecated and should never be used", "find() automatically executes JavaScript on the page"], "correct_index": 0},
                {"id": 3, "question": "What is a 'honeypot link' set by webmasters to detect scrapers?", "options": ["A link that gives users free coupons", "A link hidden from visual users (via CSS display:none) that only automated bots crawling the raw HTML click, triggering an immediate IP ban", "A link to an external honey-farming company", "A link that encrypts the user's computer"], "correct_index": 1},
                {"id": 4, "question": "Which HTTP response header indicates how many seconds a client must wait before making another request after receiving a 429 status code?", "options": ["Retry-After", "X-Wait-Time", "Rate-Limit-Sleep", "Server-Pause"], "correct_index": 0},
                {"id": 5, "question": "Why is adding randomized 'jitter' (e.g. sleep(random.uniform(1.5, 3.5))) superior to fixed sleep intervals (sleep(2)) in web scraping?", "options": ["It reduces CPU power consumption by 50%", "Fixed timing patterns create recognizable periodic spikes that rate-limiting firewalls easily flag as automated bot traffic", "Python cannot execute integer sleep durations", "It allows the scraper to run without an IP address"], "correct_index": 1},
            ]
        },
        {
            "day_number": 3,
            "title": "Day 3: Browser Automation & Dynamic SPAs with Playwright & Selenium",
            "subtopics": [
                (
                    "Headless Browser Architecture & Playwright Setup",
                    "Automate modern dynamic web applications (React, Angular, Vue) where target data is rendered asynchronously via client-side JavaScript. Understand headless browser architecture using the Chrome DevTools Protocol (CDP). Set up Playwright in Python on headless Linux EC2 servers without physical displays. Configure browser contexts, viewport sizes, and optimize memory footprints by blocking unnecessary image and font downloads.",
                    ["Configure and launch headless Chromium browsers on Linux servers using Playwright.", "Intercept and block image/font network traffic to reduce memory and accelerate scraping.", "Manage isolated browser contexts and user storage states."]
                ),
                (
                    "Dynamic Form Interaction, Infinite Scroll & Explicit Waits",
                    "Interact with dynamic UI elements reliably. Learn why time.sleep() causes fragile, slow automation. Master Explicit Waits (wait_for_selector, wait_for_load_state) that wait for precise DOM conditions. Automate multi-step form submissions, dropdowns, modal dismissals, and infinite scroll pagination by evaluating JavaScript scroll positions until content loading terminates.",
                    ["Eliminate flaky automation by replacing sleep timers with condition-based explicit waits.", "Automate complex user workflows: multi-page forms, modals, and file uploads.", "Implement infinite scroll loops that detect when dynamically loaded content terminates."]
                ),
                (
                    "Automated Screenshots, PDF Generation & File Interception",
                    "Capture visual and binary digital assets. Generate full-page screenshots of dashboards for visual monitoring and archival. Print dynamic web views into high-resolution, print-ready PDF reports. Automate binary file downloads (CSV reports, invoices), intercept download events with Playwright, and verify downloaded file integrity using MD5 checksums.",
                    ["Capture full-page and element-specific high-resolution screenshots automatically.", "Render dynamic web pages to professional PDF documents.", "Intercept browser file downloads and verify data integrity with MD5 hashing."]
                ),
            ],
            "quiz": [
                {"id": 1, "question": "Why is static HTML scraping with Requests and BeautifulSoup ineffective for single-page applications built with React or Vue?", "options": ["Because React websites do not use the HTTP protocol", "The initial HTML response contains only an empty root div and JavaScript bundle script; content is rendered client-side after script execution", "BeautifulSoup is blocked by all JavaScript frameworks", "React requires WebAssembly to download"], "correct_index": 1},
                {"id": 2, "question": "What is the primary operational hazard of using 'time.sleep(10)' to wait for dynamic elements to appear in browser automation?", "options": ["It damages the server motherboard", "It creates brittle, slow tests that fail when networks lag beyond 10 seconds and waste time when elements load in 1 second", "It forces the browser to shut down", "time.sleep() is forbidden in modern versions of Python"], "correct_index": 1},
                {"id": 3, "question": "In Playwright, what is the benefit of routing network requests to abort image and font file loading (e.g. route.abort())?", "options": ["It turns the browser into a text terminal", "It dramatically accelerates page load times and slashes server memory and bandwidth consumption", "It bypasses all website authentication gates", "It guarantees the browser will not crash on reboot"], "correct_index": 1},
                {"id": 4, "question": "What does a 'Headless' browser mode mean in server deployments?", "options": ["The browser operates without an internet connection", "The browser runs in background memory without rendering a physical graphical user interface (GUI) or display window", "The browser has no JavaScript engine", "The browser cannot store cookies"], "correct_index": 1},
                {"id": 5, "question": "Which Playwright method waits specifically until network activity has been idle for at least 500ms before continuing execution?", "options": ["page.wait_for_timeout(500)", "page.wait_for_load_state('networkidle')", "page.wait_for_server_quiet()", "page.pause_until_ready()"], "correct_index": 1},
            ]
        },
        {
            "day_number": 4,
            "title": "Day 4: Data Pipeline Automation with Pandas & Tabular Processing",
            "subtopics": [
                (
                    "Vectorized Data Transformation & ETL Pipelines",
                    "Process structured automation feeds at scale. Ingest messy tabular datasets into Pandas DataFrames. Implement vectorized data cleaning: handling missing null values (fillna, dropna), removing duplicate records, regex string standardization (formatting phone numbers, stripping currencies), type casting, and parsing heterogeneous datetime formats into standardized UTC timestamps.",
                    ["Build automated Extract, Transform, Load (ETL) data pipelines in Python.", "Execute vectorized cleaning operations orders of magnitude faster than iterative Python loops.", "Normalize messy multi-source dates and numeric strings into standardized data schemas."]
                ),
                (
                    "Excel Automation & Report Formatting with OpenPyXL",
                    "Automate corporate spreadsheet workflows. Read, create, and modify .xlsx workbooks using openpyxl. Populate multi-sheet workbooks, inject native Excel formulas (=SUM, =AVERAGE, =XLOOKUP), apply custom cell formatting (currency formats, font styling, borders, fill colors), configure conditional formatting rules, and auto-adjust column widths to fit content perfectly.",
                    ["Generate professional, stylized multi-sheet Excel reports programmatically.", "Inject dynamic spreadsheet formulas that recalculate upon opening in Excel.", "Apply conditional styling rules and auto-fit column dimensions automatically."]
                ),
                (
                    "Automated PDF Extraction & Document Processing",
                    "Extract structured data from unstructured corporate documents. Use pdfplumber and pypdf to inspect digital PDF invoices, statements, and receipts. Extract clean raw text, extract bounding box coordinates, and reconstruct complex tabular data grids into clean Pandas DataFrames. Automate text normalization across multi-page document archives.",
                    ["Extract text and tabular grids from digital PDF documents into Pandas DataFrames.", "Process multi-page invoice batches automatically without manual data entry.", "Clean and sanitize extracted document text for downstream database storage."]
                ),
            ],
            "quiz": [
                {"id": 1, "question": "Why are vectorized Pandas operations significantly faster than using standard Python for-loops to iterate over DataFrame rows?", "options": ["Pandas operations run on quantum cloud computers", "Vectorized operations are implemented in optimized, compiled C code that executes SIMD processor instructions over contiguous memory arrays", "Python for-loops delete memory every 10 rows", "Pandas converts all data into pure integer values"], "correct_index": 1},
                {"id": 2, "question": "In openpyxl, how do you insert a native Excel formula into a cell rather than a static numeric value?", "options": ["ws['C10'] = '=SUM(C2:C9)' as a string", "ws['C10'] = openpyxl.Formula('SUM', 'C2', 'C9')", "ws['C10'].calculate('SUM(C2:C9)')", "Excel formulas cannot be written using openpyxl"], "correct_index": 0},
                {"id": 3, "question": "What is the primary function of 'df.drop_duplicates(subset=['sku'], keep='last')' in a Pandas ETL pipeline?", "options": ["It drops the entire 'sku' column from the table", "It keeps only the final occurrence of duplicate rows sharing identical 'sku' values, discarding earlier duplicates", "It renames duplicate skus with numbers", "It throws an error if any duplicate skus exist"], "correct_index": 1},
                {"id": 4, "question": "What distinguishes 'pdfplumber' from basic PDF text extraction libraries like PyPDF2?", "options": ["pdfplumber is written in Java", "pdfplumber inspects precise character coordinates, bounding boxes, and lines to reconstruct tabular tables visually", "pdfplumber only works on encrypted files", "pdfplumber converts PDFs into MP3 audio files"], "correct_index": 1},
                {"id": 5, "question": "In Pandas, what does 'pd.to_datetime(df['date_str'], utc=True, errors='coerce')' do when encountering an invalid date string?", "options": ["It raises a ValueError and crashes the script", "It converts valid strings to UTC datetimes and silently converts invalid date strings into NaT (Not a Time) missing values", "It replaces invalid dates with today's date", "It deletes the entire row from memory"], "correct_index": 1},
            ]
        },
        {
            "day_number": 5,
            "title": "Day 5: API Integration, Webhooks & Automated Messaging Systems",
            "subtopics": [
                (
                    "Consuming Third-Party REST APIs & OAuth2 Workflows",
                    "Interface with external cloud services. Manage API authentication: Static API keys, Bearer tokens, and the OAuth2 Client Credentials flow. Handle cursor-based and offset-based pagination across long API collections. Inspect and respect rate-limiting headers (X-RateLimit-Remaining, X-RateLimit-Reset) and cache idempotent GET responses locally to avoid API quota burn.",
                    ["Build robust, reusable API client classes for third-party platforms.", "Implement automatic pagination to retrieve full enterprise collections.", "Parse and respect provider rate-limiting headers with intelligent pauses."]
                ),
                (
                    "Multi-Channel Alert Pipelines: Email (SMTP/cPanel), Slack & Telegram",
                    "Notify humans when critical events occur. Build multi-channel alerting engines: Dispatch rich HTML emails with embedded styles and PDF/Excel attachments using Python's smtplib and email.mime modules or transactional email APIs (cPanel/SES). Broadcast structured JSON alert webhooks to Slack channels (Block Kit formatting) and Telegram messaging bots.",
                    ["Construct and dispatch multi-part MIME emails with attachments via SMTP.", "Broadcast structured operational alert cards to Slack channels via webhooks.", "Implement fallback alerting that switches to Telegram or SMS if email dispatch fails."]
                ),
                (
                    "Building Lightweight Webhook Receivers with Flask",
                    "Create inbound event listeners that trigger automation pipelines. Build a lightweight Flask webhook endpoint to receive inbound event notifications (e.g. Stripe payment succeeded, GitHub push, Typeform submission). Validate HMAC cryptographic signatures (SHA-256) to verify webhook authenticity and reject spoofed payloads. Return immediate 200 OK responses before dispatching asynchronous background tasks.",
                    ["Build secure webhook receiver endpoints in Python with Flask.", "Verify cryptographic HMAC SHA-256 signatures to reject forged payloads.", "Return immediate 200 OK responses to avoid webhook sender timeouts."]
                ),
            ],
            "quiz": [
                {"id": 1, "question": "What is the primary purpose of verifying an HMAC SHA-256 signature header on incoming webhooks (e.g. Stripe-Signature)?", "options": ["To encrypt the outgoing response so the sender cannot read it", "To cryptographically verify that the payload originated from the authentic sender and was not intercepted or forged by an attacker", "To compress the payload size by 50%", "To check whether the sender is running on Linux"], "correct_index": 1},
                {"id": 2, "question": "Why should a webhook receiver return an HTTP 200 OK response immediately before executing long-running automation tasks?", "options": ["Webhook senders enforce strict timeouts (often 3-5 seconds); slow processing triggers automated retries and duplicate event deliveries", "HTTP 200 is the only status code allowed by the Python language", "Returning 200 saves electricity in the server rack", "Webhooks fail if any other headers are returned"], "correct_index": 0},
                {"id": 3, "question": "In Python's standard 'email.mime' library, which class is required when sending an email containing both plain text, HTML, and an attached file?", "options": ["MIMEMultipart", "MIMETextOnly", "MIMEAttachmentMaster", "MIMESingleStream"], "correct_index": 0},
                {"id": 4, "question": "What does a Slack incoming webhook require in its JSON POST payload to display formatted text?", "options": ["A JSON object containing at minimum a 'text' key or 'blocks' array", "An XML document containing a SOAP header", "A binary raw image file", "A zip file containing markdown"], "correct_index": 0},
                {"id": 5, "question": "In the OAuth2 Client Credentials grant flow, where does the application exchange its client_id and client_secret for an access_token?", "options": ["By writing them to a public GitHub repository", "Via an encrypted HTTPS POST request to the authorization server's token endpoint", "By sending an unencrypted email to the API provider", "Through a DNS TXT record lookup"], "correct_index": 1},
            ]
        },
        {
            "day_number": 6,
            "title": "Day 6: Scheduled Execution, Background Jobs & Process Daemons",
            "subtopics": [
                (
                    "Linux Cron Jobs & Systemd Timers",
                    "Automate recurring scheduled tasks on Linux servers. Understand the 5-field cron syntax (minute hour day month day-of-week). Troubleshoot classic cron failures: missing PATH environment variables, wrong working directories, and lost error logs. Transition from legacy cron to modern Linux Systemd Timers for centralized logging in journalctl, dependency chaining, and persistent miss handling across reboots.",
                    ["Schedule automation scripts reliably using Linux crontab.", "Capture scheduled job stdout and stderr into dedicated rotating log files.", "Configure Systemd service and timer unit pairs for modern scheduling."]
                ),
                (
                    "In-Process Schedulers: APScheduler & Background Workers",
                    "Embed scheduling directly inside Python applications. Use APScheduler (Advanced Python Scheduler) for interval, date, and cron triggers. Configure persistent job stores (SQLite or PostgreSQL) so scheduled jobs survive process restarts. Configure misfire grace times, coalescing missed executions, and understand concurrency trade-offs between thread pools and process pools.",
                    ["Embed background task schedulers directly within long-running Python services.", "Persist job schedules across process reboots using SQLite job stores.", "Configure misfire policies to handle jobs delayed by server load."]
                ),
                (
                    "Concurrency Control, File Locks & Idempotency",
                    "Prevent catastrophic race conditions in automated workflows. What happens when a 5-minute scheduled scraper takes 12 minutes to run? Prevent overlapping concurrent executions using file locks (fcntl.flock on Linux, portalocker) and PID tracking files. Design idempotent database mutations that safely handle repeat executions without creating duplicate records or double-charging accounts.",
                    ["Prevent overlapping script executions using operating system file locks.", "Build idempotent data operations that safely handle retries and duplicate triggers.", "Implement graceful shutdown signal handlers (SIGTERM, SIGINT) to finish transactions cleanly."]
                ),
            ],
            "quiz": [
                {"id": 1, "question": "In standard Linux cron syntax, what schedule does '0 */2 * * 1-5' represent?", "options": ["Every 2 minutes on Monday through Friday", "At minute 0 of every 2nd hour, Monday through Friday", "At 2:00 AM on the 1st and 5th day of every month", "Every 2 hours on weekends only"], "correct_index": 1},
                {"id": 2, "question": "What is the most frequent cause of a Python script working when run manually in bash, but failing when triggered via cron?", "options": ["Cron uses a minimal, restricted PATH environment variable that fails to locate the Python venv or system binaries", "Cron cannot run Python 3 scripts", "Cron requires a graphics monitor connected to the server", "Cron only runs scripts written in C"], "correct_index": 0},
                {"id": 3, "question": "Why is cross-process file locking (e.g. using fcntl.flock in non-blocking mode) essential for scheduled automation scripts?", "options": ["To encrypt the script source code from other users", "To guarantee that if a prior scheduled execution is still running, the newly spawned instance exits immediately rather than causing overlapping race conditions", "To speed up hard drive read speeds", "To prevent the operating system from shutting down"], "correct_index": 1},
                {"id": 4, "question": "In a Linux systemd timer unit, what does the setting 'Persistent=true' do?", "options": ["It keeps the timer running even when the server has no electrical power", "If the server was powered off when the scheduled timer was due, the missed service triggers immediately when the machine boots back up", "It prevents the service from ever being uninstalled", "It writes timer logs to a persistent tape drive"], "correct_index": 1},
                {"id": 5, "question": "What is the primary role of a SIGTERM signal handler in a long-running Python background worker daemon?", "options": ["To immediately kill the process without closing any files", "To intercept graceful termination requests from systemd, finish current transactional work, release database locks, and exit cleanly", "To restart the server kernel", "To send a notification to Twitter"], "correct_index": 1},
            ]
        },
        {
            "day_number": 7,
            "title": "Day 7: Production Hardening, Logging, Error Alerting & EC2 Deployment",
            "subtopics": [
                (
                    "Enterprise Logging Architecture & Rotating Handlers",
                    "Eliminate unmaintainable print() debugging statements. Configure Python's standard logging module for production: Log levels (DEBUG, INFO, WARNING, ERROR, CRITICAL), timestamp formatting, module attribution, and process IDs. Configure rotating file handlers (RotatingFileHandler by size, TimedRotatingFileHandler by day) to prevent log files from exhausting EC2 disk storage. Structure logs in JSON format for automated ingestion.",
                    ["Configure production-grade file and console logging hierarchies in Python.", "Prevent server disk exhaustion using size-based and time-based rotating log handlers.", "Format logs into structured JSON payloads for centralized log collectors."]
                ),
                (
                    "Self-Healing Automation: Retries, Dead Letter Queues & Health Checks",
                    "Design automation pipelines that survive chaos. Build custom retry decorators with jittered exponential backoff. Implement failure isolation: an exception processing record #42 should not crash the batch of 1,000 records. Route failed records into an Error Dead Letter Queue (quarantine table or file) with full traceback details for later inspection. Implement heartbeat monitoring pings (e.g. Healthchecks.io, BetterStack) to detect silent task death.",
                    ["Implement failure isolation patterns so single-item errors do not crash batch jobs.", "Route unprocessable records to dead letter quarantine queues for post-incident inspection.", "Integrate automated heartbeat healthcheck pings to alert on silent daemon failures."]
                ),
                (
                    "Headless Linux EC2 Deployment & Systemd Service Management",
                    "Deploy headless automation daemons to AWS EC2. Structure application code under /var/www/apps/automation. Configure virtual environments, isolate environment secrets, and assign restricted non-root service user ownership. Write and enable persistent Linux Systemd service unit files with Restart=always, manage automatic boot activation, and monitor real-time execution logs with journalctl.",
                    ["Deploy Python automation suites to AWS EC2 Linux instances.", "Daemonize automation workers using persistent Linux Systemd service units.", "Inspect real-time execution logs and manage process lifecycles via journalctl and systemctl."]
                ),
            ],
            "quiz": [
                {"id": 1, "question": "Why is using print() statements instead of the standard 'logging' module considered bad practice in production background daemons?", "options": ["print() is removed in modern versions of Python", "print() lacks severity levels, timestamp formatting, destination routing, and log rotation, risking disk exhaustion and lost debugging context", "print() requires an active graphical desktop monitor", "print() can only output strings shorter than 50 characters"], "correct_index": 1},
                {"id": 2, "question": "What does a TimedRotatingFileHandler with 'when=\"midnight\", backupCount=14' do?", "options": ["It deletes the application code every midnight", "It rotates the log file every night at midnight, keeping exactly the 14 most recent daily log files and deleting older ones", "It restarts the server at midnight every 14 days", "It limits logs to 14 megabytes per day"], "correct_index": 1},
                {"id": 3, "question": "What is a 'Dead Letter Queue' (DLQ) in an automated data processing pipeline?", "options": ["A folder where deleted emails are permanently erased", "A designated quarantine storage location where malformed or failed records are captured with error diagnostics without aborting the broader batch job", "A queue that automatically shuts down the EC2 instance", "An obsolete network protocol from the 1980s"], "correct_index": 1},
                {"id": 4, "question": "How does a 'heartbeat ping' (e.g. Healthchecks.io) detect that a scheduled cron job has silently stopped running?", "options": ["It sends a virus to the server", "The script sends an HTTP GET ping upon successful completion; if the monitoring service fails to receive the ping within the expected window, it dispatches an alert", "It measures the heartbeat of the human system administrator", "It restarts the server if the CPU usage drops below 1%"], "correct_index": 1},
                {"id": 5, "question": "Which Linux systemctl command both activates a service immediately AND configures it to launch automatically whenever the server boots up?", "options": ["systemctl start --now <service>", "systemctl enable --now <service>", "systemctl reboot <service>", "systemctl persist <service>"], "correct_index": 1},
            ]
        },
    ]
}

# ── Master Exports for All 9 Platform Domains (7-Day Production Curricula) ──
EXISTING_4_DOMAIN_COURSES = [
    DATA_ANALYST_COURSE,
    AI_AGENT_DEVELOPMENT_COURSE,
    FULL_STACK_DEVELOPMENT_COURSE,
    PYTHON_AUTOMATION_COURSE,
]

ALL_9_DOMAIN_COURSES = EXISTING_4_DOMAIN_COURSES + NEW_7DAY_DOMAIN_COURSES
