try {
  let num = parseInt(prompt("Enter a number: "));
  console.log(10 / num);
} catch (error) {
  console.log("An error occurred:", error.message);
}