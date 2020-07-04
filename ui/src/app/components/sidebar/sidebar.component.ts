import { Component, OnInit, Input } from '@angular/core';
import { Observable } from 'rxjs';
import { Store } from '@ngrx/store';
import {State} from '../../redux/state';
import * as AppSelectors from '../../redux/selectors';
import { Set } from 'src/app/redux/actions';
import { filter } from 'rxjs/operators';

@Component({
  selector: 'app-sidebar',
  templateUrl: './sidebar.component.html',
  styleUrls: ['./sidebar.component.scss']
})
export class SidebarComponent implements OnInit {
  open = false;

  constructor(private store: Store<State>) { }

  ngOnInit() {
    this.store.select(AppSelectors.selectUX).pipe(filter(x => x.sidebar!=null)).subscribe(ux => {
      this.open = ux.sidebar;
    })
  }

  closeSidebar() {
    this.store.dispatch(new Set({
      data: false,
      state: 'sidebar'
    }));
  }

}
