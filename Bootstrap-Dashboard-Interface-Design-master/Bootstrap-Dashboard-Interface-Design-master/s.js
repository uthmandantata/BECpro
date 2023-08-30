var createCounter = function(n) {
    return function() {
        return n++
        };    
};
console.log(createCounter(6))