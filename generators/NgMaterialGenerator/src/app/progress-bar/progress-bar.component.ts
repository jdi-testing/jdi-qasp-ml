import { Component, Input } from "@angular/core";
import { ThemePalette } from "@angular/material/core";
import { ProgressBarMode } from "@angular/material/progress-bar";

/**
 * @title Configurable progress-bar
 */
@Component({
  selector: "app-progress-bar",
  templateUrl: "./progress-bar.component.html",
  styleUrls: ["./progress-bar.component.css"],
})
export class ProgressBarComponent {
  @Input() type?: number;
  color: ThemePalette = "primary";
  mode: ProgressBarMode = "determinate";
  value = 50;
  bufferValue = 75;
}
