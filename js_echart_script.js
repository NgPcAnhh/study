// js_echart_script.js

// Process data for chart-id-118685

function processData(data) {
    
    // Combine indicators CT356 and CT20534 for "Số Bộ, ngành, địa phương đã ban hành Nghị Quyết CĐS"
    const indicator1 = data.filter(item => item.indicator === 'CT356' || item.indicator === 'CT20534');
    const combined1 = indicator1.reduce((acc, curr) => acc + curr.value, 0);
    
    // Calculate tt1
    const tt1 = combined1; // Adjust calculation as needed
    
    // Combine indicators CT360 and CT362 for "Số Bộ, ngành, địa phương đã ban hành Chương trình, Kế hoạch CĐS"
    const indicator2 = data.filter(item => item.indicator === 'CT360' || item.indicator === 'CT362');
    const combined2 = indicator2.reduce((acc, curr) => acc + curr.value, 0);
    
    // Calculate tt2
    const tt2 = combined2; // Adjust calculation as needed
    
    return { tt1, tt2 };
}

// Example usage
// const result = processData(yourDataArray); // Replace with your actual data array
// console.log(result);