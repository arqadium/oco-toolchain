using System;
using System.Windows.Forms;
using System.Security.Cryptography;
using System.IO;

namespace Checksum
{
    enum HashAlgo
    {
        None,
        SHA1,
        SHA2_256,
        SHA2_384,
        SHA2_512,
        MD5,
        CRC32
    }

    public partial class CoreForm : Form
    {
        private HashAlgo algo;

        public CoreForm(string[] args)
        {
            InitializeComponent();

            if(args.Length < 2)
            {
                return;
            }

            string hash = "";
            FileStream fs = File.Open(args[1], FileMode.Open);

            switch (args[0].ToLower())
            {
                case "sha1":
                    SHA1 sha1 = new SHA1CryptoServiceProvider();
                    foreach (byte b in sha1.ComputeHash(fs))
                    {
                        hash += b.ToString("x2").ToUpper();
                    }
                    break;
                case "sha2-256":
                    SHA256 sha256 = new SHA256CryptoServiceProvider();
                    foreach (byte b in sha256.ComputeHash(fs))
                    {
                        hash += b.ToString("x2").ToUpper();
                    }
                    break;
                case "sha2-384":
                    SHA384 sha384 = new SHA384CryptoServiceProvider();
                    foreach (byte b in sha384.ComputeHash(fs))
                    {
                        hash += b.ToString("x2").ToUpper();
                    }
                    break;
                case "sha2-512":
                    SHA512 sha512 = new SHA512CryptoServiceProvider();
                    foreach (byte b in sha512.ComputeHash(fs))
                    {
                        hash += b.ToString("x2").ToUpper();
                    }
                    break;
                case "md5":
                    MD5 md5 = new MD5CryptoServiceProvider();
                    foreach (byte b in md5.ComputeHash(fs))
                    {
                        hash += b.ToString("x2").ToUpper();
                    }
                    break;
                case "crc32":
                    CRC32 crc32 = new CRC32();
                    foreach(byte b in crc32.ComputeHash(fs))
                    {
                        hash += b.ToString("x2").ToUpper();
                    }
                    break;
                default:
                    this.algo = HashAlgo.None;
                    break;
            }

            this.hashLabel.Text = hash;
        }

        private void hashLabel_Click(object sender, EventArgs e)
        {
            Clipboard.SetText(this.hashLabel.Text);
        }
    }
}
