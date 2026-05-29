
document.addEventListener("DOMContentLoaded", function () {
  const networkLinks = {
    "LinkedIn": "https://www.linkedin.com/in/renston-jake-fernandes-9154b143",
    "ORCID": "https://orcid.org/0000-0003-2769-6397",
    "Google Scholar": "https://scholar.google.com/citations?user=2dFOscwAAAAJ&hl=en&authuser=3",
    "ResearchGate": "https://www.researchgate.net/profile/Renston-Fernandes?ev=hdr_xprf",
    "GitHub": "https://github.com/renstonferns",
    "Instagram": "https://www.instagram.com/renston_fernandes"
  };

  const section = document.querySelector("#networks");
  if (!section) return;

  Object.keys(networkLinks).forEach(function (name) {
    const headings = section.querySelectorAll("h3, h2, .feature-title, .text-lg, .font-semibold");

    headings.forEach(function (heading) {
      if (heading.textContent.trim() === name) {
        const card = heading.closest(".feature, .card, .group, .relative, .flex, div");
        if (!card) return;

        card.style.cursor = "pointer";
        card.setAttribute("role", "link");
        card.setAttribute("tabindex", "0");

        card.addEventListener("click", function () {
          window.open(networkLinks[name], "_blank", "noopener");
        });

        card.addEventListener("keydown", function (event) {
          if (event.key === "Enter" || event.key === " ") {
            event.preventDefault();
            window.open(networkLinks[name], "_blank", "noopener");
          }
        });
      }
    });
  });
});


