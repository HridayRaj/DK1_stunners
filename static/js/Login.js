/*global $, document, window, setTimeout, navigator, console, location*/

$(document).ready(function () {
  "use strict";

 
  // Detect browser for css purpose
  if (navigator.userAgent.toLowerCase().indexOf("firefox") > -1) {
    $(".form form label").addClass("fontSwitch");
  }

      // label effect
      if ($(this).val().length > 0) {
        $(this).siblings("label").addClass("active");
      } else {
        $(this).siblings("label").removeClass("active");
      }

  
  // Login steps code

  const checkButtons = (activeStep, stepsCount) => {
    const prevBtn = $("#wizard-pre");
    const nextBtn = $("#wizard-nxt");
    const submBtn = $("#wizard-sub");
  
    switch (activeStep / stepsCount) {
      case 0: // First Step
        prevBtn.hide();
        submBtn.hide();
        nextBtn.show();
        break;
      case 1: // Last Step
        nextBtn.hide();
        prevBtn.show();
        submBtn.show();
        break;
      default:
        submBtn.hide();
        prevBtn.show();
        nextBtn.show();
    }
  };
  
  // Scrolling the form to the middle of the screen if the form
  // is taller than the viewHeight
  const scrollWindow = (activeStepHeight, viewHeight) => {
    if (viewHeight < activeStepHeight) {
      $(window).scrollTop($(steps[activeStep]).offset().top - viewHeight / 2);
    }
  };
  
  // Setting the wizard body height, this is needed because
  // the steps inside of the body have position: absolute
  const setWizardHeight = activeStepHeight => {
    $(".wizard-bdy").height(activeStepHeight);
  };
  
  $(function() {
    // Form step counter (little cirecles at the top of the form)
    const wizardSteps = $(".wizard-headr .wizard-stp");
    // Form steps (actual steps)
    const steps = $(".wizard-bdy .stp");
    // Number of steps (counting from 0)
    const stepsCount = steps.length - 1;
    // Screen Height
    const viewHeight = $(window).height();
    // Current step being shown (counting from 0)
    let activeStep = 0;
    // Height of the current step
    let activeStepHeight = $(steps[activeStep]).height();
  
    checkButtons(activeStep, stepsCount);
    setWizardHeight(activeStepHeight);
    
    // Resizing wizard body when the viewport changes
    $(window).resize(function() {
      setWizardHeight($(steps[activeStep]).height());
    });
  
    // Previous button handler
    $("#wizard-pre").click(() => {
      // Sliding out current step
      $(steps[activeStep]).removeClass("activ");
      $(wizardSteps[activeStep]).removeClass("activ");
  
      activeStep--;
      
      // Sliding in previous Step
      $(steps[activeStep]).removeClass("of").addClass("activ");
      $(wizardSteps[activeStep]).addClass("activ");
  
      activeStepHeight = $(steps[activeStep]).height();
      setWizardHeight(activeStepHeight);
      checkButtons(activeStep, stepsCount);
    });
  
    // Next button handler
    $("#wizard-nxt").click(() => {
      // Sliding out current step
      $(steps[activeStep]).removeClass("initl").addClass("of").removeClass("activ");
      $(wizardSteps[activeStep]).removeClass("activ");
  
      // Next step
      activeStep++;
      
      // Sliding in next step
      $(steps[activeStep]).addClass("activ");
      $(wizardSteps[activeStep]).addClass("activ");
  
      activeStepHeight = $(steps[activeStep]).height();
      setWizardHeight(activeStepHeight);
      checkButtons(activeStep, stepsCount);
    });
  });
 


  
});




// // VUE JS Start
// var vm = new Vue({
//   el:'#locationcard',
//   data:{
//     locmethod:true,
//     gpsani:false,
//     location:false,
//     land:false,
//     res:undefined
//   },
//   methods:{
//     gps : function(){
      
//       this.locmethod = false;
//       this.gpsani = true;
      
//       if (navigator.geolocation) {
         
          
//           navigator.geolocation.getCurrentPosition(showPosition);
          
//           this.location = true;
//           this.gpsani = false;
        
//         } else { 
//           this.gpsani = false;
//           this.res = "<p>Geolocation is not supported by this browser.</p>";
//           // document.getElementById('gps').innerHTML = "Geolocation is not supported by this browser.";
          
         
//         }
//         function showPosition(position) {
          
//           document.getElementById('gps').innerHTML = "Latitude: " + position.coords.latitude + 
//           "<br>Longitude: " + position.coords.longitude ;
//           // this.res = "Latitude: " + position.coords.latitude +  "<br>Longitude: " + position.coords.longitude ;
//           document.getElementById("wizard-nxt").disabled = false;
          
          
          
//           }

      

      
//     },
//     landline : function(){
//       this.locmethod = false;
//       this.land = true;
      

      
//     },

//   }
// });
// // VUE JS End














