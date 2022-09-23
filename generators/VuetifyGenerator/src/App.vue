<template>
  <v-app>
    <v-main>
      <v-container>
        <template v-for="(component, index) in components">
          <component
            :is="component"
            :key="component"
            :data="generatedStructure[generatedComponentNamesOrder[index]]"
          />
        </template>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
import Alert from "./components/Alert";
import Badge from "./components/Badge.vue";
import AppBar from "./components/AppBar/AppBar.vue";
import ToolBar from "./components/ToolBar/ToolBar.vue";
import SystemBar from "./components/SystemBar/SystemBar.vue";
import BottomNavigation from "./components/BottomNavigation/BottomNavigation.vue";
import BottomSheet from "./components/BottomSheet/BottomSheet.vue";
import Button from "./components/Button.vue";
import Breadcrumbs from "./components/Breadcrumbs/Breadcrumbs.vue";
import Calendar from "./components/Calendar/Calendar.vue";
import Card from "./components/Card/Card.vue";
import Carousel from "./components/Carousel/Carousel.vue";
import Chip from "./components/Chip.vue";
import Dialog from "./components/Dialog/Dialog.vue";
import ExpansionPanel from "./components/ExpansionPanel/ExpansionPanel.vue";
import Autocomplete from "./components/Autocomplete.vue";
import Checkbox from "./components/Checkbox.vue";
import Combobox from "./components/Combobox.vue";
import FileInput from "./components/FileInput/FileInput.vue";
import Input from "./components/Input/Input.vue";
import OtpInput from "./components/OtpInput.vue";
import OverflowBtn from "./components/OverflowBtn.vue";
import RadioButton from "./components/RadioButton/RadioButton.vue";
import RangeSlider from "./components/RangeSlider.vue";
import Select from "./components/Select/Select.vue";
import Slider from "./components/Slider.vue";
import Switch from "./components/Switch.vue";
import TextField from "./components/TextField/TextField.vue";
import TextArea from "./components/TextArea/TextArea.vue";
import ButtonGroup from "./components/ButtonGroup/ButtonGroup.vue";
import ChipGroup from "./components/ChipGroup/ChipGroup.vue";
import SlideGroup from "./components/SlideGroup.vue";
import Window from "./components/Window/Window.vue";
import Hover from "./components/Hover/Hover.vue";
import List from "./components/List/List.vue";
import Menu from "./components/Menu/Menu.vue";
import NavigationDrawer from "./components/NavigationDrawer/NavigationDrawer.vue";
import Pagination from "./components/Pagination/Pagination.vue";
import ColorPicker from "./components/ColorPicker.vue";
import DatePicker from "./components/DatePicker/DatePicker.vue";
import DatePickerMonth from "./components/DatePickerMonth/DatePickerMonth.vue";
import TimePicker from "./components/TimePicker.vue";
import Rating from "./components/Rating.vue";
import Stepper from "./components/Stepper/Stepper.vue";
import SimpleTable from "./components/SimpleTable/SimpleTable.vue";
import DataTable from "./components/DataTable/DataTable.vue";
import Tabs from "./components/Tabs/Tabs.vue";
import Timeline from "./components/TimeLine/Timeline.vue";
import Treeview from "./components/Treeview/Treeview.vue";
import VirtualScroller from "./components/VirtualScroller/VirtualScroller.vue";

console.log(process.env);
const generatedStructure = process.env.GENERATED_STRUCTURE;
const generatedComponentNamesOrder = process.env.GENERATED_COMPONENTS_ORDER;
const components = {
  alert: Alert,
  badge: Badge,
  appBar: AppBar,
  toolBar: ToolBar,
  systemBar: SystemBar,
  bottomNavigation: BottomNavigation,
  bottomSheet: BottomSheet,
  button: Button,
  breadcrumbs: Breadcrumbs,
  calendar: Calendar,
  card: Card,
  carousel: Carousel,
  chip: Chip,
  dialog: Dialog,
  expansionPanel: ExpansionPanel,
  autocomplete: Autocomplete,
  checkbox: Checkbox,
  combobox: Combobox,
  fileInput: FileInput,
  input: Input,
  otpInput: OtpInput,
  overflowBtn: OverflowBtn,
  radioButton: RadioButton,
  rangeSlider: RangeSlider,
  select: Select,
  slider: Slider,
  switch: Switch,
  textField: TextField,
  textArea: TextArea,
  buttonGroup: ButtonGroup,
  chipGroup: ChipGroup,
  slideGroup: SlideGroup,
  window: Window,
  hover: Hover,
  list: List,
  menu: Menu,
  navigationDrawer: NavigationDrawer,
  pagination: Pagination,
  colorPicker: ColorPicker,
  datePicker: DatePicker,
  datePickerMonth: DatePickerMonth,
  timePicker: TimePicker,
  rating: Rating,
  stepper: Stepper,
  simpleTable: SimpleTable,
  dataTable: DataTable,
  tabs: Tabs,
  timeline: Timeline,
  treeview: Treeview,
  virtualScroller: VirtualScroller,
};

export default {
  name: "App",

  components: {
    ...Object.values(components),
  },

  data: () => ({
    generatedStructure,
    generatedComponentNamesOrder,
  }),

  computed: {
    components() {
      return generatedComponentNamesOrder.map(
        (componentName) => components[componentName]
      );
    },
  },
};
</script>
