// Theme custom js methods
$(document).ready(function(){

  // Custom for descriptions in some programmes
  var addTotalsNote = function(){
    var notes = {
      'es': 'Se incluyen únicamente los gastos e ingresos no financieros, es decir, capítulos I al VII.',
      'eu': 'Gastu eta diru-sarrera ez finantzarioak bakarrik sartu dira, hau da I-VII kapituluak.',
    };

    var lang = $('html').attr('lang') || 'es';

    $('#totals-panel .budget-totals .text-center small').html( notes[lang] );
  };

  addTotalsNote();
});


// Override
// Calculate global budget indicators
function calculateIndicators(chapterBreakdown, budgetStatuses, adjustInflationFn, uiState) {
  function format(amount) {
    return formatAmount(adjustInflationFn(amount, uiState.year));
  }

  var gross_savings = getSum(chapterBreakdown, _.range(1, 5), 'income', uiState.year, budgetStatuses) -
                      getSum(chapterBreakdown, [1, 2, 4], 'expense', uiState.year, budgetStatuses);
  var net_savings = gross_savings - getSum(chapterBreakdown, [3, 9], 'expense', uiState.year, budgetStatuses);
  var funding_capacity = getSum(chapterBreakdown, _.range(1, 7), 'income', uiState.year, budgetStatuses) -
                          getSum(chapterBreakdown, _.range(1, 7), 'expense', uiState.year, budgetStatuses);

  $('#total-gross-savings').text(format(gross_savings));
  $('#total-net-savings').text(format(net_savings));
  $('#total-funding-capacity').text(format(funding_capacity));

  $('#indicators-year, #totals-year').text(uiState.year);
}
