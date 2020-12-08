// specialty form function
function addSpecialtySection () {
    
    let div = document.getElementById("js");
    let template = document.getElementById("html");
    let specialtySection = document.createElement("section");
    let index = div.childNodes.length + 1;

    specialtySection.setAttribute("id", "specialties" + index);
    specialtySection.innerHTML = template.innerHTML;
    div.appendChild(specialtySection);

    let specialtyInput = specialtySection.childNodes[5];
    let other = specialtySection.childNodes[7];
    
    specialtyInput.addEventListener ("change", function() {
      console.log('hi')
      if (specialtyInput.value == "Other") {
        other.style.display = "block";
      } else {
        other.style.display = "none";
      }
    });
  }

  addSpecialtySection(); 

// success form function
function thankYou () {
  
  let div = document.getElementById("thank-you");
  div.style.display = "";
}

thankYou();