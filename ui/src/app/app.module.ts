import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent, NgbdModalContent } from './app.component';
import {NgbModule} from '@ng-bootstrap/ng-bootstrap';
import { ReactiveFormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';
import { AppService } from './app.service';
import { SettingsComponent } from './components/settings/settings.component';
import { SidebarComponent } from './components/sidebar/sidebar.component';
import { GraphComponent } from './components/graph/graph.component';
import { DataService } from './services/data.service';
import { StoreModule } from '@ngrx/store';
import { EffectsModule } from '@ngrx/effects';
import { AppEffects } from './redux/effects';
import * as AppReducers from './redux/reducers';
// import { offlineMetaReducer } from './redux/offline.metareducer';
import { SimpleNotificationsModule } from 'angular2-notifications';
import {BrowserAnimationsModule} from '@angular/platform-browser/animations';
import { StoreDevtoolsModule } from '@ngrx/store-devtools';
import { environment } from 'src/environments/environment';
import { SliderComponent } from './components/slider/slider.component';
import { NgxSliderModule } from '@angular-slider/ngx-slider'
@NgModule({
  declarations: [
    AppComponent,
    NgbdModalContent,
    SettingsComponent,
    SidebarComponent,
    GraphComponent,
    SliderComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    NgbModule,
    ReactiveFormsModule,
    HttpClientModule,
    StoreModule.forRoot(
      AppReducers.reducers,
      // { 
      //   metaReducers: [offlineMetaReducer] 
      // }
    ),
    StoreDevtoolsModule.instrument({
      maxAge: 25, // Retains last 25 states
      logOnly: environment.production, // Restrict extension to log-only mode
    }),
    EffectsModule.forRoot([AppEffects]),
    SimpleNotificationsModule.forRoot(),
    BrowserAnimationsModule,
    NgxSliderModule
  ],
  providers: [
    // AppService,
    // DataService
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
