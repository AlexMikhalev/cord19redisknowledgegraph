import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Store } from '@ngrx/store';
import { Create, Set } from 'src/app/redux/actions';
import { State } from 'src/app/redux/state';

@Component({
  selector: 'app-search-form',
  templateUrl: './search-form.component.html',
  styleUrls: ['./search-form.component.scss']
})
export class SearchFormComponent implements OnInit {

  searchForm: FormGroup;

  // searches
  // "Effectiveness of case isolation/isolation of exposed individuals (i.e. quarantine)",
  // "Effectiveness of community contact reduction",
  // "Effectiveness of inter/inner travel restriction",
  // "Effectiveness of school distancing",
  // "Effectiveness of workplace distancing",
  // "Effectiveness of a multifactorial strategy prevent secondary transmission",
  // "Seasonality of transmission",
  // "How does temperature and humidity affect the transmission of 2019-nCoV?",
  // "Significant changes in transmissibility in changing seasons?",
  // "Effectiveness of personal protective equipment (PPE)"
  
  constructor(private store: Store<State>, fb: FormBuilder) { 

    this.searchForm = fb.group({
      'term': ['', Validators.required]
      // 'term': ['following variants', Validators.required]
    });
  }

  ngOnInit() {
  }

  search(){
    if(this.searchForm.valid){

      // create search request
      this.store.dispatch(new Create({
        data: { search: this.searchForm.get('term').value },
        state: 'searchResults',
        postProcess: 'map:years', 
        route: 'gsearch'
      }));

      // set search term
      this.store.dispatch(new Set({
        data: this.searchForm.get('term').value,
        state: 'searchTerm'
      }));
    }
  }
}
