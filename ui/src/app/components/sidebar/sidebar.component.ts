import { Component, OnInit, Input } from '@angular/core';
import { Store } from '@ngrx/store';
import {State} from '../../redux/state';
import * as AppSelectors from '../../redux/selectors';
import { Set } from 'src/app/redux/actions';
import { filter, map, distinctUntilChanged } from 'rxjs/operators';

@Component({
  selector: 'app-sidebar',
  templateUrl: './sidebar.component.html',
  styleUrls: ['./sidebar.component.scss']
})
export class SidebarComponent implements OnInit {
  open = false;
  selected: any;
  edgeData$: any;

  constructor(private store: Store<State>) { }

  ngOnInit() {
    this.store.select(AppSelectors.selectUX)
      .pipe(map(x => x.sidebar))
      .pipe(distinctUntilChanged())
      .pipe(filter(x => x!=null))
      .subscribe(open => {
        this.open = open;
      }
    );

    this.store.select(AppSelectors.selectedEvent)
      .pipe(distinctUntilChanged())
      .pipe(filter(x => x!=null))
      .subscribe(selected => {
        this.selected = selected;
      }
    );

    this.edgeData$ = this.store.select(AppSelectors.selectEdgeResults);
  }

  closeSidebar() {
    this.store.dispatch(new Set({
      data: false,
      state: 'sidebar'
    }));
  }

}
