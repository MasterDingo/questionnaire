Vue.component('answer', {
  data: function() {
    return {
      answer_id: "answer-"+this.answerValue,
      answer_text: this.text,
      selectedValue: this.value
    };
  },
  props: {
    answerValue: Number,
    text: String,
    value: Number
  },
  template: `
   <div class="answer">
     <input type="radio" name="answer" :id="answer_id" v-model="selectedValue" :value="answerValue" @change="$emit('input', selectedValue)">
     <label :for="answer_id" v-text="answer_text"></label>
   </div>
  `
});

Vue.component('question', {
  props: {
    text: String,
    answers: Array,
    value: Number
  },
  data: function() {
    return {
      selectedAnswer: this.value
    };
  },
  template: `
  <div id="question">
    <p>{{ text }}</p>
    <answer v-for="answer in answers" :key="answer.id" :answer-value="answer.id" :text="answer.text" v-model="selectedAnswer" @input="$emit('input', selectedAnswer)"></answer>
    <button @click="$emit('got-answer', selectedAnswer)">Choose</button>
  </div>
  `
});

var app = new Vue({
  delimiters: ['[[', ']]'],
  el: "#app",
  data: {
    question_text: "The question",
    answers_data: [],
    answer: 0
  },
  methods: {
    sendAnswer: function() {
      var vm = this;
      fetch('http://192.168.56.101:8888/api/v1/answer/',
        {
          method: 'POST',
          headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({id: this.answer})
        }
      ).then((response) => {
        if(response.ok)
          return response.json();
      })
      .then(vm.parseJson);
    },
    startQuiz: function() {
      var vm = this;
      fetch('http://192.168.56.101:8888/api/v1/question/')
        .then((response) => {
          if(response.ok)
            return response.json();
        })
        .then(vm.parseJson);
    },
    parseJson: function(json) {
      var vm = this;
      console.log(json);
      vm.question_text = json.text;
      vm.answers_data = json.answers;
      console.log(vm);
    }
  },
  created: function() {
    this.startQuiz();
  }
});
