import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormControl, FormGroup } from '@angular/forms';
import { Options } from '@angular-slider/ngx-slider';
import { debounceTime, filter } from 'rxjs/operators';
import { Store } from '@ngrx/store';

import { State } from '../../redux/state';
import { Create } from 'src/app/redux/actions';
import * as AppSelectors from '../../redux/selectors';

@Component({
  selector: 'app-slider',
  templateUrl: './slider.component.html',
  styleUrls: ['./slider.component.scss']
})
export class SliderComponent implements OnInit {
  form: FormGroup;
  initYear = 2001;
  searchTerm = '';
  options: Options = {
    floor: this.initYear
  };

  constructor(fb: FormBuilder, private store: Store<State>) {
    this.form = fb.group({
      year: new FormControl(this.initYear)
    });
  }

  reset() {
    this.form.reset(this.initYear)
  }



  ngOnInit() {
    this.form.valueChanges.pipe(debounceTime(500)).subscribe(snapshot => {
      this.fetchFilteredData(snapshot.year)
    })

    this.store.select<any>(AppSelectors.selectSearchResults)
      .pipe(filter(x => x!=null))
      .subscribe((results) => {
        this.changeSliderOptions(results.years)
      }
    );

    this.store.select<any>(AppSelectors.selectSearchTerm)
      .pipe(filter(x => x!=null))
      .subscribe((term) => {
        this.searchTerm = term
      }
    );
  }

  changeSliderOptions(years) {
    const newOptions: Options = Object.assign({}, this.options);
    newOptions.stepsArray = years.map((year: string) => {
      return { value: year }
    });
    // 
    this.options = newOptions;
  }
  

  fetchFilteredData(year) {
    // dispatch redux action
    this.store.dispatch(new Create({
      data: { years: [year], search: this.searchTerm },
      state: 'searchResults',
      route: 'gsearch'
    }));
  }

}
