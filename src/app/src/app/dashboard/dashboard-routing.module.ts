import {NgModule} from '@angular/core';
import {RouterModule, Routes} from '@angular/router';
import {DashboardComponent} from "./dashboard.component";
import {DatasetComponent, AddDatasetComponent, EditDatasetComponent} from "./components";
import {NumberAttributesStepComponent} from "./components/number-attributes-step/number-attributes-step.component";
import {CategoricalAttributesStepComponent} from "./components/categorical-attributes-step/categorical-attributes-step.component";

const routes: Routes = [
  {
    path: 'dashboard', component: DashboardComponent,
    children: [
      {path: '', redirectTo: 'datasets', pathMatch: 'full'},
      {path: 'datasets', component: DatasetComponent},
      {path: 'add-dataset', component: AddDatasetComponent},
      {
        path: 'edit-dataset', component: EditDatasetComponent, children: [
          {path: '', redirectTo: 'categorical-attributes', pathMatch: 'full'},
          {path: 'number-attributes', component: NumberAttributesStepComponent},
          {path: 'categorical-attributes', component: CategoricalAttributesStepComponent},
        ]
      },
    ]
  }];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class DashboardRoutingModule {
}