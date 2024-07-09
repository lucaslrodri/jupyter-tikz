document.querySelectorAll("a").forEach(function(element){
    let href = element.getAttribute("href");
    
    // Check to see if the the href include http:// or https://
    if (href){
      if(href.includes("https://") || href.includes("http://")){
        element.target = "_blank"; // Make link open in new tab
        element.rel = "noreferrer nofollow noopener"; 
  
        console.log(element); // Just for testing
      }
    }
  });