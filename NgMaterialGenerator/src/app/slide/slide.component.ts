import { Component, Input } from "@angular/core";
import { ThemePalette } from "@angular/material/core";

/**
 * @title Configurable slide-toggle
 */
@Component({
  selector: "app-slide",
  templateUrl: "./slide.component.html",
  styleUrls: ["./slide.component.css"],
})
export class SlideComponent {
  @Input() type?: number;
  color: ThemePalette = "accent";
  checked = false;
  disabled = false;
}
