using System;
using System.Collections.Generic;
using System.IO;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace argos_pbtail
{
    public partial class fmMain : Form
    {
        //private delegate void SafeLog1Delegate(string text);
        //private delegate void SafeLog2Delegate(string text);
        //private delegate void SafeLog3Delegate(string text);

        public fmMain()
        {
            InitializeComponent();
        }

        private void Form1_Load(object sender, EventArgs e)
        {
            tm.Enabled = true;
            bgw1.RunWorkerAsync();
            bgw2.RunWorkerAsync();
            bgw3.RunWorkerAsync();
        }
        private void tm_Tick(object sender, EventArgs e)
        {
            if (!bgw1.IsBusy)
            {
                tm.Enabled = false;
                bgw3.CancelAsync();
                bgw2.CancelAsync();
                this.Close();
            }
        }

        private void bgw1_DoWork(object sender, DoWorkEventArgs e)
        {
            int cnt = 0;
            var logfile = Environment.GetFolderPath(Environment.SpecialFolder.UserProfile) + "\\.argos-rpa.sta.1";
            while (!File.Exists(logfile))
            {
                Thread.Sleep(500);
                cnt += 1;
                if (cnt > 10)
                    return;
            }
            FileStream fs = File.Open(logfile, FileMode.Open, FileAccess.Read, FileShare.ReadWrite);
            using (StreamReader reader = new StreamReader(fs, Encoding.UTF8))
            {
                string line;
                while (true)
                {
                    if ((line = reader.ReadLine()) != null)
                    {
                        line = line.TrimEnd('\n');
                        Invoke(new MethodInvoker(() =>
                        {
                            log1.Text = line;
                        }));
                        if (line == "Preparing STU and PAM is done.")
                            return;
                    }
                    else
                    {
                        Thread.Sleep(500);
                    }
                }
            }
        }

        private void bgw2_DoWork(object sender, DoWorkEventArgs e)
        {
            var logfile = Environment.GetFolderPath(Environment.SpecialFolder.UserProfile) + "\\.argos-rpa.sta.2";
            while (!File.Exists(logfile))
            {
                Thread.Sleep(1);
            }
            FileStream fs = File.Open(logfile, FileMode.Open, FileAccess.Read, FileShare.ReadWrite);
            using (StreamReader reader = new StreamReader(fs, Encoding.UTF8))
            {
                string line;
                while (true)
                {
                    if ((line = reader.ReadLine()) != null)
                    {
                        line = line.TrimEnd('\n');
                        Invoke(new MethodInvoker(() =>
                        {
                            log2.Text = line;
                        }));
                    }
                    else
                    {
                        Thread.Sleep(500);
                    }
                }
            }
        }

        private void bgw3_DoWork(object sender, DoWorkEventArgs e)
        {
            var logfile = Environment.GetFolderPath(Environment.SpecialFolder.UserProfile) + "\\.argos-rpa.sta.3";
            while (!File.Exists(logfile))
            {
                Thread.Sleep(1);
            }
            FileStream fs = File.Open(logfile, FileMode.Open, FileAccess.Read, FileShare.ReadWrite);
            using (StreamReader reader = new StreamReader(fs, Encoding.UTF8))
            {
                string line;
                while (true)
                {
                    if ((line = reader.ReadLine()) != null)
                    {
                        line = line.TrimEnd('\n');
                        Invoke(new MethodInvoker(() =>
                        {
                            log3.Text = line;
                        }));
                    }
                    else
                    {
                        Thread.Sleep(500);
                    }
                }
            }
        }

    }
}
