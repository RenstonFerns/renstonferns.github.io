---
title: "Dr. Renston Jake Fernandes | Professional Portfolio"
summary: "Portfolio of Dr. Renston Jake Fernandes — clean fuels, LCA, TEA, combustion, and e-fuels innovation."
date: 2026-05-28
type: landing
sections:
  - block: dev-hero
    content:
        username: admin
        greeting: "Hello, I'm"
        title: Dr. Renston Jake Fernandes
        tagline: "Clean Fuels | E-Fuels | LCA | TEA | Aspen Plus | Combustion"
        bio: "I develop integrated process modelling, life-cycle assessment, and techno-economic frameworks for circular carbon e-fuels from biomass, residues, and captured CO₂. My work connects Aspen Plus simulation, GREET/Sphera-based LCA, TEA, uncertainty analysis, and combustion assessment to support sustainable transport fuel strategies."
        cta_buttons:
          - text: Connect on LinkedIn
            url: "https://www.linkedin.com/in/renston-jake-fernandes-9154b143"
            icon: brands/linkedin
          - text: Download Full CV
            url: /uploads/resume.pdf
            icon: document-arrow-down
        typewriter:
          enable: true
          prefix: I research on
          strings:
            - clean e-fuels
            - circular carbon solutions
            - life cycle assessment
            - Techno-economic analysis
            - sustainable transport
            - process modelling
          type_speed: 65
          delete_speed: 35
          pause_time: 2200
        show_status: true
        show_scroll_indicator: true
        links:
          - icon: brands/github
            url: "https://github.com/renstonfernandes"
            label: GitHub
          - icon: brands/linkedin
            url: "https://www.linkedin.com/in/renstonfernandes"
            label: LinkedIn
          - icon: academicons/orcid
            url: "https://orcid.org/0000-0003-2769-6397"
            label: ORCID
          - icon: academicons/researchgate
            url: "https://www.researchgate.net/profile/Renston-Fernandes?ev=hdr_xprf"
            label: ResearchGate
    design:
        style: centered
        avatar_shape: circle
        animations: true
        background:
          color:
            light: "#f8fafc"
            dark: "#0c0e1a"
          gradient_mesh:
            enable: true
            style: orbs
            colors:
              - primary-600/30
              - secondary-600/20
              - accent-400/30
            orb_count: 3
            animation: pulse
            intensity: bold
    id: hero
    - block: features
    content:
      title: "Find Me Online"
      subtitle: "Research profiles, professional networks, and project repositories"
      items:
        - name: "LinkedIn"
          description: "Professional updates & networking"
          icon: brands/linkedin
          url: "https://www.linkedin.com/in/renston-jake-fernandes-9154b143"

        - name: "ORCID"
          description: "Researcher identity & publication record"
          icon: academicons/orcid
          url: "https://orcid.org/0000-0003-2769-6397"

        - name: "Google Scholar"
          description: "Citation metrics & scholarly works"
          icon: academicons/google_scholar
          url: "https://scholar.google.com/citations?user=2dFOscwAAAAJ&hl=en&authuser=3"

        - name: "ResearchGate"
          description: "Collaborations & open research"
          icon: academicons/researchgate
          url: "https://www.researchgate.net/profile/Renston-Fernandes?ev=hdr_xprf"

        - name: "GitHub"
          description: "Code, tools, and datasets"
          icon: brands/github
          url: "https://github.com/renstonferns"

        - name: "Instagram"
          description: "Science outreach, music, and creative work"
          icon: brands/instagram
          url: "https://www.instagram.com/renston_fernandes"
    design:
      background:
        color:
          light: "#f4fbfa"
          dark: "#081f2a"
    id: networks
  - block: tech-stack
    content:
        title: Technical Expertise
        subtitle: "Key tools, platforms, and software"
        categories:
          - name: "Process & LCA Tools"
            items:
                - name: Aspen Plus
                  icon: custom/aspen-plus
                - name: Sphera (GaBi)
                  icon: custom/sphera
                - name: GREET
                  icon: custom/greet
          - name: "Simulation & Analysis"
            items:
                - name: MATLAB
                  icon: devicon/matlab
                - name: Python
                  icon: devicon/python
          - name: "Modelling & CAD"
            items:
                - name: COMSOL
                  icon: custom/comsol
                - name: SolidWorks
                  icon: custom/solidworks
          - name: Writing
            items:
                - name: Overleaf
                  icon: custom/overleaf
    design:
        style: grid
        show_levels: false
        background:
          color:
            light: "#f5f5f5"
            dark: "#0d0d12"
    id: skills
  - block: stats
    content:
        title: Impact by the Numbers
        items:
          - statistic: 50+
            description: Citations
            icon: academicons/google-scholar
          - statistic: 12+
            description: Peer-reviewed Publications
            icon: hero/document-text
          - statistic: 20+
            description: "Talks & Presentations"
            icon: hero/microphone
          - statistic: 4
            description: Research Grants
            icon: hero/award
    design:
        layout: cards
        background:
          gradient:
            start: primary-700
            end: secondary-700
            direction: 135
          text_color_light: true
    id: impact
    demo: false
  - block: markdown
    content:
        title: "Research Philosophy & Vision"
        text:
          |
            My research journey blends process design, sustainability, and real-world industrial application. I specialize in process simulation, techno-economic analysis (TEA), and LCA for circular-carbon and biomass-derived fuel systems.  
            
            **Current Achievements**: Aspen Plus models for integrated biomass-to-e-methanol, CO₂ capture, and hydrogen production, validated against industrial benchmarks and coupled with Monte Carlo uncertainty analysis for cost hotspot identification.
            
            **Future Vision**: Extend expertise into integrated gasification-electrolysis-synthesis process modeling to develop validated pathways for advanced fuel production from waste and residues, bridging the gap between laboratory research and industry.
    id: research
  - block: markdown
    content:
        title: "Teaching & Mentorship"
        text:
          |
            "I view teaching as an opportunity to ignite curiosity and build confidence in students by guiding them through authentic, hands-on engineering challenges."
            
            My philosophy centers on active, problem-based learning and project cycles. I've taught modules from Fluid Mechanics to Non-Conventional Energy Sources, pairing lectures with lab projects. Every class aims for clarity so even high-schoolers can be engaged and empowered.
    id: teaching
  - block: resume-experience
    content:
        username: admin
        text: "Career highlights — roles, education, and notable milestones."
    design:
        date_format: Jan 2006
        is_education_first: true
    id: experience
  - block: features
    content:
        title: Selected Accomplishments
        items:
          - name: KAUST PhD Fellowship
            description: Full funding awarded 2021–2026.
            icon: hero/star
          - name: Sussex India Scholarship
            description: Awarded for M.Sc. academic excellence.
            icon: hero/academic-cap
          - name: KSCST State Grants
            description: Funding for renewable fuel experimentation.
            icon: hero/arrow-trending-up
          - name: "Music & Production"
            description: "Co-founded 'The Speksy Pscyentist', releases on Spotify."
            icon: hero/musical-note
    id: accomplishments
  - block: contact-info
    content:
        title: "Let's Work Together"
        subtitle: "Open to collaborations, consulting, and fuel assessment"
        email: "renston.fernandes@kaust.edu.sa"
        social:
          - icon: brands/linkedin
            url: "https://www.linkedin.com/in/renstonfernandes"
          - icon: academicons/orcid
            url: "https://orcid.org/0000-0003-2769-6397"
          - icon: brands/github
            url: "https://github.com/renstonfernandes"
          - icon: academicons/researchgate
            url: "https://www.researchgate.net/profile/Renston_Fernandes"
        text: "I am open to research collaborations, industry consulting, and policy-relevant fuel assessment. Reach out for partnerships or guest speaking."
    id: contact
---
