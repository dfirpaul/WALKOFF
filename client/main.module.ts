import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule }   from '@angular/forms';
import { HttpModule } from '@angular/http';

// Custom routing module
import { RoutingModule } from './routing';
import { MainComponent } from './main/main.component';
import { ControllerComponent } from './controller/controller.component';
import { CasesComponent } from './cases/cases.component';
import { SettingsComponent } from './settings/settings.component';

@NgModule({
	imports: [
		BrowserModule,
		FormsModule,
		HttpModule,
		RoutingModule,
	],
	declarations: [
		MainComponent,
		ControllerComponent,
		CasesComponent,
		SettingsComponent,
	],
	bootstrap: [MainComponent]
})
export class MainModule { }