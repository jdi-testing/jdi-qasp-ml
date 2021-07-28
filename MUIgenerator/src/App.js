import { JDIchips } from "./controls/Chip";
import { JDICheckbox } from "./controls/Checkbox";
import { JDIContainer } from "./controls/Container";
import { JDIAvatar } from "./controls/Avatar";
import JDICard from "./controls/Card";
import JDIradio from "./controls/Radio";
import JDIAppBar from "./controls/appBar";
import JDIstepper from "./controls/Stepper";
import JDISlider from "./controls/Slider";
import JDITabs from "./controls/Tabs";
import { JDITable } from "./controls/table/Table";
import JDIAlert from "./controls/Alert";
import JDIBackdrop from "./controls/Backdrop";
import { JDIGrid } from "./controls/grid/Grid";
import { JDIList } from "./controls/list/List";
import { JDIDivider } from "./controls/Divider";
import { JDIDialog } from "./controls/dialog/Dialog";
import JDIDateTimePickers from "./controls/DateTimePicker";
import { JDISelect } from "./controls/select/Select";
import JDISwitch from "./controls/Switch";
import JDIButtonGroup from "./controls/ButtonGroup";
import { JDIDrawer } from "./controls/Drawer/Drawer";
import JDIBreadcrumbs from "./controls/Breadcrumbs";
import JDIBottomNavigation from "./controls/BottomNavigation";
import { JDIAccordeon } from "./controls/accordion/Accordion";
import JDIPortal from "./controls/Portal";
import JDITextarea from "./controls/Textarea";
import { JDIPopover } from "./controls/Popover/Popover";
import JDIPopper from "./controls/Popper";
import JDICircular from "./controls/Circular";
import JDILink from "./controls/Link";
import JDIMenu from "./controls/Menu";
import JDITextField from "./controls/TextField";
import { JDIBox } from "./controls/Box";
import JDIBadge from "./controls/Badge";
import JDISnackbar from "./controls/Snackbar";

const controlParams = JSON.parse(process.env.REACT_APP_NOT_SECRET_CODE);

function App() {
  console.log(controlParams);
  return (
    <div>
      <JDIAccordeon {...controlParams.Accordion} />
      <JDIAlert {...controlParams.Alert} />
      <JDIAppBar {...controlParams.AppBar} />
      <JDIAvatar {...controlParams.Avatar} />
      <JDIBackdrop {...controlParams.Backdrop} />
      <JDIBadge {...controlParams.Badge} />
      <JDIButtonGroup {...controlParams.ButtonGroup} />
      <JDIBreadcrumbs {...controlParams.Breadcrumbs} />
      <JDIBottomNavigation {...controlParams.BottomNavigation} />
      <JDIBox />
      <JDICard {...controlParams.Card} />
      <JDICircular {...controlParams.Circular} />
      <JDICheckbox {...controlParams.Checkbox} />
      <JDIchips {...controlParams.Chip} />
      <JDIContainer {...controlParams.Container} />
      <JDIDateTimePickers {...controlParams.DateTimePicker} />
      <JDIDialog {...controlParams.Dialog} />
      <JDIDivider {...controlParams.Divider} />
      <JDIDrawer {...controlParams.Drawer} />
      <JDIGrid {...controlParams.Grid} />
      <JDILink {...controlParams.Link} />
      <JDIList {...controlParams.List} />
      <JDIMenu {...controlParams.Menu} />
      <JDIPortal />
      <JDIPopover {...controlParams.Popover} />
      <JDIPopper {...controlParams.Popper} />
      <JDIradio {...controlParams.Radio} />
      <JDISelect {...controlParams.Select} />
      <JDIstepper {...controlParams.Stepper} />
      <JDISlider {...controlParams.Slider} />
      <JDISnackbar {...controlParams.Snackbar} />
      <JDISwitch {...controlParams.Switch} />
      <JDITabs {...controlParams.Tabs} />
      <JDITable {...controlParams.Table} />
      <JDITextarea {...controlParams.TextArea} />
      <JDITextField {...controlParams.TextField} />
    </div>
  );
}

export default App;
