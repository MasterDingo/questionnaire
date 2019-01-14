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
  <div class="question">
    <p>{{ text }}</p>
    <div class="answer-list">
      <answer v-for="answer in answers" :key="answer.id" :answer-value="answer.id" :text="answer.text" v-model="selectedAnswer" @input="$emit('input', selectedAnswer)"></answer>
    </div>
    <div class="button">
      <button v-if="answers.length>0" @click="$emit('got-answer', selectedAnswer)" >Choose</button>
      <button v-if="answers.length==0" @click="$emit('restart-quiz')">Restart</button>
    </div>
  </div>
  `
});

var app = new Vue({
  delimiters: ['[[', ']]'],
  el: "#app",
  data: {
    question_text: "The question",
    answers_data: [],
    answer: 0,
    loading: false
  },
  methods: {
    sendAnswer: function() {
      var vm = this;
      vm.loading = true;
      fetch('http://192.168.56.101:8888/api/v1/question/',
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
      .then(function(json) {
        console.log(this);
        vm.loadQuestion(json.next_id);
      });
    },
    loadQuestion: function(quest_id) {
      var vm = this;
      var url = 'http://192.168.56.101:8888/api/v1/question/';
      if(typeof quest_id != 'undefined') {
        url+= quest_id+'/';
      }
      vm.loading = true;
      fetch(url)
        .then((response) => {
          if(response.ok)
            return response.json();
        })
        .then(vm.parseJson);
    },
    parseJson: function(json) {
      var vm = this;
      vm.question_text = json.text;
      vm.answers_data = json.answers;
      vm.loading = false;
    }
  },
  created: function() {
    this.loadQuestion();
  }
});
