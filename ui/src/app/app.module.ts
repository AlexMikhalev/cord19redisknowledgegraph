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

@NgModule({
  declarations: [
    AppComponent,
    NgbdModalContent,
    SettingsComponent,
    SidebarComponent,
    GraphComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    NgbModule,
    ReactiveFormsModule,
    HttpClientModule
  ],
  providers: [
    AppService
  ],
  bootstrap: [AppComponent],
  entryComponents: [NgbdModalContent]
})
export class AppModule { }
