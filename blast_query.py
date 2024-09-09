from Bio.Blast.Applications import NcbiblastpCommandline
from io import StringIO
from Bio.Blast import NCBIXML

def blast_query(query_sequence):
    # Define BLASTP command parameters
    blastp_cline = NcbiblastpCommandline(db="blastp_db_toy/toy_viro3d_seq_db.fas", outfmt=5, num_threads=4)
    
    # Execute BLASTP search
    stdout, stderr = blastp_cline(stdin=query_sequence, stdout=True, stderr=True)
    
    if stderr:
        print(f"Error occurred: {stderr}")
        return None
    
    # Parse BLASTP output
    result_handle = StringIO(stdout)
    blast_records = NCBIXML.parse(result_handle)
    
    # Process BLAST records here (e.g., print, save to file, etc.)
    for record in blast_records:
        # Example: Print query ID and descriptions of top hits
        print(f"Query: {record.query}")
        for alignment in record.alignments:
            for hsp in alignment.hsps:
                print(f"Subject: {alignment.hit_def}, Score: {hsp.score} Positives: {hsp.positives}, gaps: {hsp.gaps}")
    
    return blast_records

seq = 'MSASKEIKSFLWTQSLRRELSGYCSNIKLQVVKDAQALLHGLDFSEVSNVQRLMRKERRDDNDLKRLRDLNQAVNNLVELKSTQQKSILRVGTLTSDDLLILAADLEKLKSKVIRTERPLSAGVYMGNLSSQQLDQRRALLNMIGMSGGNQGARAGRDGVVRVWDVKNAELLNNQFGTMPSLTLACLTKQGQVDLNDAVQALTDLGLIYTAKYPNTSDLDRLTQSHPILNMIDTKKSSLNISGYNFSLGAAVKAGACMLDGGNMLETIKVSPQTMDGILKSILKVKKALGMFISDTPGERNPYENILYKICLSGDGWPYIASRTSITGRAWENTVVDLESDGKPQKADSNNSSKSLQSAGFTAGLTYSQLMTLKDAMLQLDPNAKTWMDIEGRPEDPVEIALYQPSSGCYIHFFREPTDLKQFKQDAKYSHGIDVTDLFATQPGLTSAVIDALPRNMVITCQGSDDIRKLLESQGRKDIKLIDIALSKTDSRKYENAVWDQYKDLCHMHTGVVVEKKKRGGKEEITPHCALMDCIMFDAAVSGGLNTSVLRAVLPRDMVFRTSTPRVVL'

blast_query(seq)

# def blast_query(query_sequence):

#     cmd = f"echo ${query_sequence} | blastp -db viro3d_blast_db -out results.xml -outfmt 5"
