document.getElementById('generatePDF').addEventListener('click', function () {
    const { jsPDF } = window.jspdf;
    const doc = new jsPDF();

    // Set report title
    doc.setFontSize(18);
    doc.text("Monthly Case Summary Report", 10, 10);

    // Add case statistics
    const totalCases = document.getElementById('totalCases').innerText;
    const solvedCases = document.getElementById('solvedCases').innerText;
    const pendingCases = document.getElementById('pendingCases').innerText;

    doc.setFontSize(12);
    doc.text(`Total Cases: ${totalCases}`, 10, 30);
    doc.text(`Solved Cases: ${solvedCases}`, 10, 40);
    doc.text(`Pending Cases: ${pendingCases}`, 10, 50);

    // Add priority breakdown
    const highPriority = document.getElementById('highPriority').innerText;
    const mediumPriority = document.getElementById('mediumPriority').innerText;
    const lowPriority = document.getElementById('lowPriority').innerText;

    doc.text("Priority Breakdown", 10, 70);
    doc.text(`High Priority: ${highPriority}`, 10, 80);
    doc.text(`Medium Priority: ${mediumPriority}`, 10, 90);
    doc.text(`Low Priority: ${lowPriority}`, 10, 100);

    // Save the PDF
    doc.save('Monthly_Case_Summary_Report.pdf');
});
