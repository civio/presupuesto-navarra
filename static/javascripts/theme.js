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