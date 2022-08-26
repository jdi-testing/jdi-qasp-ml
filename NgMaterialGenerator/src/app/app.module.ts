import { NgModule } from "@angular/core";
import { BrowserModule } from "@angular/platform-browser";

import { AppComponent } from "./app.component";
import { BrowserAnimationsModule } from "@angular/platform-browser/animations";

import { FormsModule, ReactiveFormsModule } from "@angular/forms";
import { MatAutocompleteModule } from "@angular/material/autocomplete";
import { MatFormFieldModule } from "@angular/material/form-field";
import { MatInputModule } from "@angular/material/input";
import { MatBadgeModule } from "@angular/material/badge";
import { MatButtonModule } from "@angular/material/button";
import { MatIconModule } from "@angular/material/icon";
import { MatDividerModule } from "@angular/material/divider";
import { MatButtonToggleModule } from "@angular/material/button-toggle";
import { MatCardModule } from "@angular/material/card";
import { MatCheckboxModule } from "@angular/material/checkbox";
import { MatChipsModule } from "@angular/material/chips";
import { MatDatepickerModule } from "@angular/material/datepicker";
import { MatDialogModule } from "@angular/material/dialog";
import { MatListModule } from "@angular/material/list";
import { MatExpansionModule } from "@angular/material/expansion";
import { MatSelectModule } from "@angular/material/select";
import { MatRadioModule } from "@angular/material/radio";
import { MatGridListModule } from "@angular/material/grid-list";
import { MatMenuModule } from "@angular/material/menu";
import { MatPaginatorModule } from "@angular/material/paginator";
import { MatProgressBarModule } from "@angular/material/progress-bar";
import { MatProgressSpinnerModule } from "@angular/material/progress-spinner";
import { MatSlideToggleModule } from "@angular/material/slide-toggle";
import { MatSliderModule } from "@angular/material/slider";
import { MatSortModule } from "@angular/material/sort";
import { MatStepperModule } from "@angular/material/stepper";
import { MatTableModule } from "@angular/material/table";
import { MatTabsModule } from "@angular/material/tabs";
import { MatToolbarModule } from "@angular/material/toolbar";
import { MatTreeModule } from "@angular/material/tree";
import { MatSidenavModule } from "@angular/material/sidenav";
import { MatSnackBarModule } from "@angular/material/snack-bar";

import { DragDropModule } from "@angular/cdk/drag-drop";

import { AutocompleteHighlightComponent } from "./autocomplete/autocomplete-highlight/autocomplete-highlight.component";
import { AutocompleteFilterComponent } from "./autocomplete/autocomplete-filter/autocomplete-filter.component";
import { AutocompleteGroupsComponent } from "./autocomplete/autocomplete-groups/autocomplete-groups.component";
import { AutocompletePlainInputComponent } from "./autocomplete/autocomplete-plain-input/autocomplete-plain-input.component";
import { AutocompleteComponent } from "./autocomplete/autocomplete.component";
import { ButtonComponent } from "./button/button.component";
import { ButtonToggleComponent } from "./button-toggle/button-toggle.component";
import { CardSectionedComponent } from "./card/card-sectioned/card-sectioned.component";
import { CardComponent } from "./card/card.component";
import { CardSimpleComponent } from "./card/card-simple/card-simple.component";
import { CheckboxComponent } from "./checkbox/checkbox.component";
import { ChipsBasicComponent } from "./chips/chips-basic/chips-basic.component";
import { ChipsComponent } from "./chips/chips.component";
import { ChipsStackedComponent } from "./chips/chips-stacked/chips-stacked.component";
import { ChipsDndComponent } from "./chips/chips-dnd/chips-dnd.component";
import { ChipsAutocompleteComponent } from "./chips/chips-autocomplete/chips-autocomplete.component";
import { DatepickerComponent } from "./datepicker/datepicker.component";
import { DatepickerRangeComponent } from "./datepicker/datepicker-range/datepicker-range.component";
import { MatNativeDateModule } from "@angular/material/core";
import { DatepickerFormsComponent } from "./datepicker/datepicker-forms/datepicker-forms.component";
import { DatepickerCustomFormatComponent } from "./datepicker/datepicker-custom-format/datepicker-custom-format.component";
import { DatepickerBasicComponent } from "./datepicker/datepicker-basic/datepicker-basic.component";
import { DividerComponent } from "./divider/divider.component";
import { ExpansionPanelComponent } from "./expansion-panel/expansion-panel.component";
import { ExpansionPanelBasicComponent } from "./expansion-panel/expansion-panel-basic/expansion-panel-basic.component";
import { ExpansionPanelAccordionComponent } from "./expansion-panel/expansion-panel-accordion/expansion-panel-accordion.component";
import { FormFieldComponent } from "./form-field/form-field.component";
import { GridListComponent } from "./grid-list/grid-list.component";
import { InputComponent } from "./input/input.component";
import { ListComponent } from "./list/list.component";
import { PaginatorComponent } from "./paginator/paginator.component";
import { ProgressBarComponent } from "./progress-bar/progress-bar.component";
import { SpinnerComponent } from "./spinner/spinner.component";
import { RadioComponent } from "./radio/radio.component";
import { SlideComponent } from "./slide/slide.component";
import { SliderComponent } from "./slider/slider.component";
import { SortHeaderComponent } from "./sort-header/sort-header.component";
import { StepperComponent } from "./stepper/stepper.component";
import { StepperBasicComponent } from "./stepper/stepper-basic/stepper-basic.component";
import { StepperLazyComponent } from "./stepper/stepper-lazy/stepper-lazy.component";
import { StepperCustomizedComponent } from "./stepper/stepper-customized/stepper-customized.component";
import { TableComponent } from "./table/table.component";
import { TableBasicComponent } from "./table/table-basic/table-basic.component";
import { TableMultHeaderComponent } from "./table/table-mult-header/table-mult-header.component";
import { TablePaginatedComponent } from "./table/table-paginated/table-paginated.component";
import { TableStickyComponent } from "./table/table-sticky/table-sticky.component";
import { TabsComponent } from "./tabs/tabs.component";
import { ToolbarComponent } from "./toolbar/toolbar.component";
import { TreeComponent } from "./tree/tree.component";
import { TreeFlatComponent } from "./tree/tree-flat/tree-flat.component";
import { TreeCheckboxesComponent } from "./tree/tree-checkboxes/tree-checkboxes.component";
import { BottomSheetComponent } from "./bottom-sheet/bottom-sheet.component";
import { DialogComponent } from "./dialog/dialog.component";
import { MenuComponent } from "./menu/menu.component";
import { SelectComponent } from "./select/select.component";
import { SidenavComponent } from "./sidenav/sidenav.component";
import { SnackbarComponent } from "./snackbar/snackbar.component";

@NgModule({
  declarations: [
    AppComponent,
    AutocompleteHighlightComponent,
    AutocompleteFilterComponent,
    AutocompleteGroupsComponent,
    AutocompletePlainInputComponent,
    AutocompleteComponent,
    ButtonComponent,
    ButtonToggleComponent,
    CardSectionedComponent,
    CardComponent,
    CardSimpleComponent,
    CheckboxComponent,
    ChipsBasicComponent,
    ChipsComponent,
    ChipsStackedComponent,
    ChipsDndComponent,
    ChipsAutocompleteComponent,
    DatepickerComponent,
    DatepickerRangeComponent,
    DatepickerFormsComponent,
    DatepickerCustomFormatComponent,
    DatepickerBasicComponent,
    DividerComponent,
    ExpansionPanelComponent,
    ExpansionPanelBasicComponent,
    ExpansionPanelAccordionComponent,
    FormFieldComponent,
    GridListComponent,
    InputComponent,
    ListComponent,
    PaginatorComponent,
    ProgressBarComponent,
    SpinnerComponent,
    RadioComponent,
    SlideComponent,
    SliderComponent,
    SortHeaderComponent,
    StepperComponent,
    StepperBasicComponent,
    StepperLazyComponent,
    StepperCustomizedComponent,
    TableComponent,
    TableBasicComponent,
    TableMultHeaderComponent,
    TablePaginatedComponent,
    TableStickyComponent,
    TabsComponent,
    ToolbarComponent,
    TreeComponent,
    TreeFlatComponent,
    TreeCheckboxesComponent,
    BottomSheetComponent,
    DialogComponent,
    MenuComponent,
    SelectComponent,
    SidenavComponent,
    SnackbarComponent,
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    FormsModule,
    DragDropModule,
    MatFormFieldModule,
    MatInputModule,
    ReactiveFormsModule,
    MatAutocompleteModule,
    MatBadgeModule,
    MatButtonModule,
    MatIconModule,
    MatDividerModule,
    MatButtonToggleModule,
    MatCardModule,
    MatCheckboxModule,
    MatChipsModule,
    MatDatepickerModule,
    MatNativeDateModule,
    MatDialogModule,
    MatListModule,
    MatExpansionModule,
    MatSelectModule,
    MatRadioModule,
    MatGridListModule,
    MatMenuModule,
    MatPaginatorModule,
    MatProgressBarModule,
    MatProgressSpinnerModule,
    MatSlideToggleModule,
    MatSliderModule,
    MatSortModule,
    MatStepperModule,
    MatTableModule,
    MatTabsModule,
    MatToolbarModule,
    MatTreeModule,
    MatSidenavModule,
    MatSnackBarModule,
  ],
  providers: [MatDatepickerModule],
  bootstrap: [AppComponent],
})
export class AppModule {}
