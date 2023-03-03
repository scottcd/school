
namespace MipsPipelineUI {
    partial class AboutControlForm {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing) {
            if (disposing && (components != null)) {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent() {
            this.label1 = new System.Windows.Forms.Label();
            this.ControlBox = new System.Windows.Forms.ComboBox();
            this.label2 = new System.Windows.Forms.Label();
            this.InstructionOneLabel = new System.Windows.Forms.Label();
            this.DescriptionLabel = new System.Windows.Forms.Label();
            this.label3 = new System.Windows.Forms.Label();
            this.SuspendLayout();
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Font = new System.Drawing.Font("Segoe UI", 14F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point);
            this.label1.Location = new System.Drawing.Point(21, 23);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(173, 25);
            this.label1.TabIndex = 3;
            this.label1.Text = "MIPS Control Logic";
            // 
            // ControlBox
            // 
            this.ControlBox.FormattingEnabled = true;
            this.ControlBox.Location = new System.Drawing.Point(200, 25);
            this.ControlBox.Name = "ControlBox";
            this.ControlBox.Size = new System.Drawing.Size(121, 23);
            this.ControlBox.TabIndex = 4;
            this.ControlBox.SelectedValueChanged += new System.EventHandler(this.InstructionComboBox_SelectionChangeCommitted);
            // 
            // label2
            // 
            this.label2.AutoSize = true;
            this.label2.Font = new System.Drawing.Font("Segoe UI", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point);
            this.label2.Location = new System.Drawing.Point(31, 58);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(121, 21);
            this.label2.TabIndex = 5;
            this.label2.Text = "Example Syntax:";
            // 
            // InstructionOneLabel
            // 
            this.InstructionOneLabel.AutoSize = true;
            this.InstructionOneLabel.Location = new System.Drawing.Point(31, 83);
            this.InstructionOneLabel.Name = "InstructionOneLabel";
            this.InstructionOneLabel.Size = new System.Drawing.Size(38, 15);
            this.InstructionOneLabel.TabIndex = 6;
            this.InstructionOneLabel.Text = "label3";
            // 
            // DescriptionLabel
            // 
            this.DescriptionLabel.AutoSize = true;
            this.DescriptionLabel.Location = new System.Drawing.Point(31, 140);
            this.DescriptionLabel.Name = "DescriptionLabel";
            this.DescriptionLabel.Size = new System.Drawing.Size(38, 15);
            this.DescriptionLabel.TabIndex = 8;
            this.DescriptionLabel.Text = "label4";
            // 
            // label3
            // 
            this.label3.AutoSize = true;
            this.label3.Font = new System.Drawing.Font("Segoe UI", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point);
            this.label3.Location = new System.Drawing.Point(31, 119);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(92, 21);
            this.label3.TabIndex = 14;
            this.label3.Text = "Description:";
            // 
            // AboutControlForm
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(7F, 15F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(384, 186);
            this.Controls.Add(this.label3);
            this.Controls.Add(this.DescriptionLabel);
            this.Controls.Add(this.InstructionOneLabel);
            this.Controls.Add(this.label2);
            this.Controls.Add(this.label1);
            this.Controls.Add(this.ControlBox);
            this.Name = "AboutControlForm";
            this.Text = "AboutControl";
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.ComboBox ControlBox;
        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.Label InstructionOneLabel;
        private System.Windows.Forms.Label DescriptionLabel;
        private System.Windows.Forms.Label label3;
    }
}