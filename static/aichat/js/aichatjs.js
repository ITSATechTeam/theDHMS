function moveNumbersToNextLine(sentence) {
    // Use regular expression to find all numbers (\d+)
    // and replace them with a newline character followed by the number
    return sentence.replace(/\b(\d+)\b/g, '\n$1');
}

const sentence = "This is a sample sentence with 123 numbers scattered 456 throughout.";
const result = moveNumbersToNextLine(sentence);

console.log(result);
