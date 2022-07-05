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
import JDIButton from "./controls/button/Button";
import JDIInputBase from "./controls/InputBase";
import JDIModal from "./controls/Modal";

const controlParams = JSON.parse(process.env.REACT_APP_GENERATED_STRUCTURE);

function App() {
  const renderControls = () => {
    const controls = [];
    controlParams.forEach(({ key, value }) => {
      const control =
        (key === 'Accordion' && <JDIAccordeon {...value} />) ||
        (key === "Alert" && <JDIAlert {...value} />) ||
        (key === "AppBar" && <JDIAppBar {...value} />) ||
        (key === "Avatar" && <JDIAvatar {...value} />) ||
        (key === "Backdrop" && <JDIBackdrop {...value} />) ||
        (key === "Badge" && <JDIBadge {...value} />) ||
        (key === "Button" && <JDIButton {...value} />) ||
        (key === "ButtonGroup" && <JDIButtonGroup {...value} />) ||
        (key === "Breadcrumbs" && <JDIBreadcrumbs {...value} />) ||
        (key === "BottomNavigation" && <JDIBottomNavigation {...value} />) ||
        (key === "Box" && <JDIBox />) ||
        (key === "Card" && <JDICard {...value} />) ||
        (key === "Circular" && <JDICircular {...value} />) ||
        (key === "Checkbox" && <JDICheckbox {...value} />) ||
        (key === "Chip" && <JDIchips {...value} />) ||
        (key === "Container" && <JDIContainer {...value} />) ||
        (key === "DateTimePicker" && <JDIDateTimePickers {...value} />) ||
        (key === "Dialog" && <JDIDialog {...value} />) ||
        (key === "Divider" && <JDIDivider {...value} />) ||
        (key === "Drawer" && <JDIDrawer {...value} />) ||
        (key === "Grid" && <JDIGrid {...value} />) ||
        (key === "InputBase" && <JDIInputBase {...value} />) ||
        (key === "Link" && <JDILink {...value} />) ||
        (key === "List" && <JDIList {...value} />) ||
        (key === "Menu" && <JDIMenu {...value} />) ||
        (key === "Modal" && <JDIModal {...value} />) ||
        (key === "Portal" && <JDIPortal />) ||
        (key === "Popover" && <JDIPopover {...value} />) ||
        (key === "Popper" && <JDIPopper {...value} />) ||
        (key === "Radio" && <JDIradio {...value} />) ||
        (key === "Select" && <JDISelect {...value} />) ||
        (key === "Stepper" && <JDIstepper {...value} />) ||
        (key === "Slider" && <JDISlider {...value} />) ||
        (key === "Snackbar" && <JDISnackbar {...value} />) ||
        (key === "Switch" && <JDISwitch {...value} />) ||
        (key === "Tabs" && <JDITabs {...value} />) ||
        (key === "Table" && <JDITable {...value} />) ||
        (key === "TextArea" && <JDITextarea {...value} />) ||
        (key === "TextField" && <JDITextField {...value} />);
      controls.push(control);
    })
    return controls;
  }

  return (
    <div>
      {
        renderControls()
      }
    </div>
  );
}

export default App;
