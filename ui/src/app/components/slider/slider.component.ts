import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormControl, FormGroup } from '@angular/forms';
import { Options } from '@angular-slider/ngx-slider';
import { debounceTime } from 'rxjs/operators';
import { Store } from '@ngrx/store';

import { State } from '../../redux/state';
import { Create } from 'src/app/redux/actions';

@Component({
  selector: 'app-slider',
  templateUrl: './slider.component.html',
  styleUrls: ['./slider.component.scss']
})
export class SliderComponent implements OnInit {
  form: FormGroup;
  minValue = 50;
  maxValue = 200;
  options: Options = {
    floor: 0,
    ceil: 250,
    step: 5
  };

  constructor(fb: FormBuilder, private store: Store<State>) {
    this.form = fb.group({
      sliderControl: new FormControl([this.minValue, this.maxValue])
    });
  }

  reset() {
    this.form.reset({ sliderControl: [this.minValue, this.maxValue]})
  }



  ngOnInit() {
    this.form.valueChanges.pipe(debounceTime(500)).subscribe(snapshot => {
      console.log("From reactive form");
      console.log(snapshot);
    })
  }

  fetchFilteredData(startValue, endValue) {
    // dispatch redux action
    this.store.dispatch(new Create({
      data: { start: startValue, end: endValue },
      state: 'searchResults',
      route: 'gsearch'
    }));
  }

}
