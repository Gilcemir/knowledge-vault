/* Reusable quiz component for lessons.
   Usage in a lesson:
     <div class="quiz" data-answer="2">
       <p class="quiz-q">Question text?</p>
       <button class="quiz-opt">Option A</button>
       <button class="quiz-opt">Option B</button>
       <button class="quiz-opt">Option C</button>
       <p class="quiz-explain">Why the answer is what it is.</p>
     </div>
   data-answer is the 0-based index of the correct option.
   Include once per lesson: <script src="../assets/quiz.js" defer></script>
*/
document.addEventListener('DOMContentLoaded', function () {
  document.querySelectorAll('.quiz').forEach(function (quiz) {
    var answer = parseInt(quiz.dataset.answer, 10);
    var opts = quiz.querySelectorAll('.quiz-opt');
    opts.forEach(function (btn, i) {
      btn.addEventListener('click', function () {
        if (quiz.classList.contains('answered')) return;
        quiz.classList.add('answered');
        if (i === answer) {
          btn.classList.add('correct');
        } else {
          btn.classList.add('incorrect');
          opts[answer].classList.add('correct');
        }
        opts.forEach(function (b) { b.disabled = true; });
      });
    });
  });
});
